"""
Meta Conversions API — серверная отправка событий о заявках в Meta (Facebook/
Instagram Ads), в дополнение к браузерному Meta Pixel (события не теряются
из-за блокировщиков рекламы/ITP/третьих кук).

Что отправляется: событие "Lead" при создании заказа коврика (mat_order) или
заказа товара (product_order) — см. LeadSerializer.create() в serializers.py.
Жалобы (complaint) сознательно не отправляются — не тот сигнал, на который
нужно оптимизировать таргетинг рекламы.

В custom_data кладётся не только факт заявки, а конкретный товар за ней
(content_ids/content_name/contents — см. _content_data): для коврика это
конкретная модель авто (id вида "car-model-<pk>"), для товара — вариант
товара ("product-variant-<pk>"). Это даёт Meta данные для последующего
динамического ретаргетинга ("вот тот самый коврик, который вы смотрели") —
но только если товар потом ещё и загружен как отдельный каталог в Meta
Commerce Manager, что в этом проекте пока не сделано (отдельная задача,
не относится к Conversions API как таковому).

Настройка: META_PIXEL_ID/META_ACCESS_TOKEN берутся из .env (см.
config/settings.py). Пока они не заданы (Pixel и токен ещё не созданы в Meta
Business Manager), send_lead_event() — no-op: не бросает исключений, ничего
не делает. Как только появятся боевые значения — интеграция включится сама,
без изменений кода.

Хеширование: Meta требует, чтобы персональные данные (телефон, email и т.п.)
приходили только в виде SHA-256 от нормализованного значения — сырые данные
слать нельзя. У нас сейчас есть только телефон (Lead.phone); email нигде не
собирается (осознанное решение — не усложнять форму заявки), поэтому match
rate будет ниже, чем при полном наборе полей, но это ожидаемо.

Отправка — синхронная (requests, короткий timeout), в отдельном потоке,
чтобы не задерживать ответ API заявителю; сетевые ошибки только логируются,
никогда не всплывают наружу и не мешают созданию заявки.
"""

import hashlib
import logging
import threading
import time

import requests
from django.conf import settings

from .models import Lead

logger = logging.getLogger(__name__)

API_VERSION = 'v21.0'
REQUEST_TIMEOUT = 5  # секунд


def _hash(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode('utf-8')).hexdigest()


def _normalize_phone(phone: str) -> str:
    """Только цифры, без +/пробелов/дефисов — так, как требует Meta."""
    return ''.join(ch for ch in phone if ch.isdigit())


def _content_data(lead, total_price) -> dict:
    """content_ids/contents — какой именно товар за этим событием, а не
    просто факт заявки. id формируются так, чтобы не пересекаться между
    ковриками (по модели авто) и товарами (по варианту) в одном каталоге."""
    if lead.lead_type == Lead.TYPE_MAT_ORDER and lead.car_model:
        return {
            'content_ids': [f'car-model-{lead.car_model_id}'],
            'content_name': f'{lead.car_model.brand.name} {lead.car_model.name}',
            'content_type': 'product',
            'contents': [{'id': f'car-model-{lead.car_model_id}', 'quantity': 1, 'item_price': float(total_price or 0)}],
        }
    if lead.lead_type == Lead.TYPE_PRODUCT_ORDER and lead.product_variant:
        return {
            'content_ids': [f'product-variant-{lead.product_variant_id}'],
            'content_name': lead.product_variant.product.name,
            'content_type': 'product',
            'contents': [{
                'id': f'product-variant-{lead.product_variant_id}', 'quantity': 1,
                'item_price': float(total_price or 0),
            }],
        }
    return {}


def _build_payload(lead, request, total_price) -> dict:
    user_data = {}
    if lead.phone:
        user_data['ph'] = [_hash(_normalize_phone(lead.phone))]

    if request is not None:
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        if ip:
            user_data['client_ip_address'] = ip.split(',')[0].strip()
        ua = request.META.get('HTTP_USER_AGENT', '')
        if ua:
            user_data['client_user_agent'] = ua
        # fbc/fbp — куки браузерного Meta Pixel; фронт должен передавать их
        # вместе с заявкой (полей fbc/fbp пока нет в LeadSerializer — см. README).
        fbc = request.data.get('fbc') if hasattr(request, 'data') else None
        fbp = request.data.get('fbp') if hasattr(request, 'data') else None
        if fbc:
            user_data['fbc'] = fbc
        if fbp:
            user_data['fbp'] = fbp

    event_source_url = request.data.get('event_source_url', '') if request is not None and hasattr(request, 'data') else ''

    event = {
        'event_name': 'Lead',
        'event_time': int(time.time()),
        'event_id': f'lead-{lead.id}',  # дедупликация с браузерным Pixel, если фронт шлёт тот же id
        'action_source': 'website',
        'user_data': user_data,
        'custom_data': {
            'content_category': lead.lead_type,
            'currency': 'USD',
            'value': float(total_price) if total_price else 0,
            **_content_data(lead, total_price),
        },
    }
    if event_source_url:
        event['event_source_url'] = event_source_url

    payload = {'data': [event]}
    if settings.META_TEST_EVENT_CODE:
        payload['test_event_code'] = settings.META_TEST_EVENT_CODE
    return payload


def _send(payload: dict) -> None:
    url = f'https://graph.facebook.com/{API_VERSION}/{settings.META_PIXEL_ID}/events'
    try:
        r = requests.post(url, params={'access_token': settings.META_ACCESS_TOKEN}, json=payload, timeout=REQUEST_TIMEOUT)
        if r.status_code >= 400:
            logger.warning('Meta CAPI: %s %s', r.status_code, r.text[:500])
    except requests.RequestException:
        logger.exception('Meta CAPI: сетевая ошибка при отправке события')


def send_lead_event(lead, request=None, total_price=None) -> None:
    """Отправляет событие Lead в Meta CAPI для заказа коврика/товара.
    Не блокирует вызывающий код и не бросает исключений — фоновый поток."""
    if not settings.META_PIXEL_ID or not settings.META_ACCESS_TOKEN:
        return
    if lead.lead_type not in (lead.TYPE_MAT_ORDER, lead.TYPE_PRODUCT_ORDER):
        return

    payload = _build_payload(lead, request, total_price)
    threading.Thread(target=_send, args=(payload,), daemon=True).start()
