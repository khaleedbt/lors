from urllib.parse import urlparse

from django.conf import settings
from rest_framework.permissions import BasePermission


def request_origin(request) -> str | None:
    """Origin запроса — из заголовка Origin, с фоллбэком на Referer для
    нестандартных клиентов, которые шлют только его. Настоящий браузер на
    кросс-доменном fetch/XHR POST (а это ровно наш случай — фронтенд и
    бэкенд на разных доменах) ВСЕГДА шлёт Origin сам, без участия фронтенда."""
    origin = request.headers.get('Origin')
    if origin:
        return origin
    referer = request.headers.get('Referer')
    if not referer:
        return None
    parsed = urlparse(referer)
    if not parsed.scheme or not parsed.netloc:
        return None
    return f'{parsed.scheme}://{parsed.netloc}'


def is_allowed_origin(request) -> bool:
    origin = request_origin(request)
    return origin is not None and origin in settings.CORS_ALLOWED_ORIGINS


class OriginAllowed(BasePermission):
    """Доп. слой поверх throttling (см. views.py) на публичных write-
    эндпоинтах (Lead/Review). НЕ настоящая защита от целенаправленной
    атаки — Origin обычный заголовок, любой скрипт может подставить туда
    что угодно. Смысл — отсеять generic-спам-ботов, которые просто долбят
    найденный POST-эндпоинт без Origin/Referer вообще или с чужого
    домена, не заточенных именно под lorssy.com."""
    message = 'Запрос должен приходить с разрешённого домена сайта.'

    def has_permission(self, request, view):
        return is_allowed_origin(request)
