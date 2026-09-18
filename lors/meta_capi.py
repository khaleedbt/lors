"""
Meta Conversions API (CAPI) — серверное дублирование событий, которые
браузерный Meta Pixel шлёт с фронтенда (lorssy-frontend, src/lib/metaPixel.ts).
Так события не теряются из-за блокировщиков рекламы/ITP/Link Tracking
Protection и клика по WhatsApp, уводящего со страницы быстрее, чем успевает
уйти обычный fetch без keepalive.

Дедупликация у Meta работает по паре (event_name, event_id) в окне 48 часов.
КРИТИЧНО: event_id генерируется на фронте (один раз на действие) и приходит
сюда уже готовым — сервер НИКОГДА не придумывает свой event_id для того же
события. Раньше здесь так и было (send_lead_event() генерировал "lead-<id>"
при создании Lead, независимо от браузерного вызова) — событие уходило в
Meta дважды с разными id, дедупликация не работала (это и было причиной
диагностики в Events Manager «Improve your rate of Meta Pixel events covered
by Conversions API»). Теперь единственная точка входа — /api/meta-event/,
которую фронт дёргает сам, передавая тот же event_id, что ушёл в fbq().

Настройка: META_PIXEL_ID/META_ACCESS_TOKEN из .env (см. config/settings.py).
Пока не заданы — send_to_meta() тихо no-op'ится, эндпоинт всё равно отвечает
204 (фронту не с чем разбираться). META_PIXEL_ID здесь же используется как
dataset id — в Meta это один и тот же числовой идентификатор.
"""

import hashlib
import logging
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from django.core.cache import cache
from rest_framework.throttling import BaseThrottle

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

API_VERSION = 'v25.0'  # версия из ТЗ/референс-реализации lorssy-frontend
REQUEST_TIMEOUT = 5  # секунд

# Публичный эндпоинт — без белого списка в датасет можно залить что угодно.
ALLOWED_EVENT_NAMES = {
    'PageView', 'ViewContent', 'Search', 'Lead', 'Contact', 'AddToCart',
    'CustomizeProduct', 'InitiateCheckout', 'CompleteRegistration',
}

# Bounded workers and queue: do not spawn a thread for every public request.
_RATE_LIMIT = 60
_RATE_WINDOW = 60
_sender = ThreadPoolExecutor(max_workers=4, thread_name_prefix='meta-capi')
_sender_slots = threading.BoundedSemaphore(16)


def is_rate_limited(ip: str) -> bool:
    key = 'meta-rate:' + hashlib.sha256(ip.encode()).hexdigest()
    # Fixed windows bound cache lifetime; nginx supplies the strict ingress limit.
    key += ':' + str(int(time.time()) // _RATE_WINDOW)
    if cache.add(key, 1, timeout=_RATE_WINDOW * 2):
        return False
    try:
        return cache.incr(key) > _RATE_LIMIT
    except ValueError:
        return True


def _send_with_slot(event):
    try:
        send_to_meta(event)
    finally:
        _sender_slots.release()


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def normalize_phone(raw: str) -> str | None:
    """'0912345678' -> '963912345678' (best-effort под сирийские номера)."""
    if not raw:
        return None
    digits = re.sub(r'[^\d+]', '', raw)
    if digits.startswith('+'):
        digits = digits[1:]
    if digits.startswith('00'):
        digits = digits[2:]
    if digits.startswith('0'):
        digits = '963' + digits[1:]
    return digits or None


def _normalize_text(raw: str | None) -> str | None:
    if not raw:
        return None
    return raw.strip().lower() or None


def get_client_ip(request) -> str | None:
    return BaseThrottle().get_ident(request)


def _derive_fbc_from_url(url: str) -> str | None:
    match = re.search(r'[?&]fbclid=([^&]+)', url or '')
    if not match:
        return None
    return f'fb.1.{int(time.time() * 1000)}.{match.group(1)}'


def build_user_data(request, user: dict, event_source_url: str) -> dict:
    """Хешированный PII + сигналы браузера/сети. Пустые поля не включаются
    вовсе — иначе Event Match Quality у события падает."""
    data: dict[str, str] = {}

    phone = normalize_phone(user.get('phone', ''))
    if phone:
        data['ph'] = _sha256(phone)

    email = _normalize_text(user.get('email'))
    if email:
        data['em'] = _sha256(email)

    first_name = _normalize_text(user.get('firstName'))
    if first_name:
        data['fn'] = _sha256(first_name)

    last_name = _normalize_text(user.get('lastName'))
    if last_name:
        data['ln'] = _sha256(last_name)

    city = _normalize_text(user.get('city'))
    if city:
        data['ct'] = _sha256(re.sub(r'\s+', '', city))

    country = _normalize_text(user.get('country'))
    if country:
        data['country'] = _sha256(country)

    external_id = user.get('externalId')
    if external_id:
        data['external_id'] = _sha256(str(external_id))

    # Не хешируются — это сигналы браузера/сети, не PII в чистом виде.
    fbp = request.COOKIES.get('_fbp')
    if fbp:
        data['fbp'] = fbp

    fbc = request.COOKIES.get('_fbc') or _derive_fbc_from_url(event_source_url)
    if fbc:
        data['fbc'] = fbc

    ip = get_client_ip(request)
    if ip:
        data['client_ip_address'] = ip

    ua = request.META.get('HTTP_USER_AGENT')
    if ua:
        data['client_user_agent'] = ua

    return data


def send_to_meta(event: dict) -> None:
    """Синхронно, с ретраями — вызывающая view оборачивает в поток, чтобы
    не задерживать ответ клиенту (см. views.MetaEventView)."""
    if not settings.META_PIXEL_ID or not settings.META_ACCESS_TOKEN:
        return

    payload = {'data': [event]}
    if settings.META_TEST_EVENT_CODE:
        payload['test_event_code'] = settings.META_TEST_EVENT_CODE

    url = f'https://graph.facebook.com/{API_VERSION}/{settings.META_PIXEL_ID}/events'
    delays = [0, 0.3, 0.6]  # первая попытка сразу, потом 300мс, потом 600мс
    for attempt, delay in enumerate(delays):
        if delay:
            time.sleep(delay)
        try:
            r = requests.post(
                url, params={'access_token': settings.META_ACCESS_TOKEN},
                json=payload, timeout=REQUEST_TIMEOUT,
            )
        except requests.RequestException as exc:
            if attempt < len(delays) - 1:
                continue
            logger.error(
                'meta CAPI network error name=%s id=%s error=%s',
                event.get('event_name'), event.get('event_id'), exc,
            )
            return

        if r.status_code < 400:
            return
        if r.status_code in (429, 500, 502, 503, 504) and attempt < len(delays) - 1:
            continue  # ретраим только 5xx/429
        # 4xx — ошибка в данных, ретраить бессмысленно
        logger.error(
            'meta CAPI rejected event name=%s id=%s status=%s body=%s',
            event.get('event_name'), event.get('event_id'), r.status_code, r.text[:500],
        )
        return


def build_and_send(request, body: dict) -> None:
    """Валидирует тело запроса от фронта и, если всё ок, шлёт в Meta в
    фоновом потоке (не блокирует ответ клиенту)."""
    from .serializers import MetaEventSerializer

    serializer = MetaEventSerializer(data=body)
    if not serializer.is_valid():
        return
    body = serializer.validated_data
    event_name = body['eventName']
    event_id = body['eventId']
    event_source_url = body.get('eventSourceUrl', '')
    event = {
        'event_name': event_name,
        'event_time': int(time.time()),
        'event_id': event_id,
        'event_source_url': event_source_url,
        'action_source': 'website',
        'user_data': build_user_data(request, body.get('user', {}), event_source_url),
    }
    if body.get('customData'):
        event['custom_data'] = body['customData']
    if not settings.META_PIXEL_ID or not settings.META_ACCESS_TOKEN:
        return
    if not _sender_slots.acquire(blocking=False):
        return
    try:
        _sender.submit(_send_with_slot, event)
    except Exception:
        _sender_slots.release()
        logger.exception('Unable to queue Meta event')
