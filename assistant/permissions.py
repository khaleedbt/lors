from django.conf import settings
from rest_framework import permissions


class HasAssistantKey(permissions.BasePermission):
    """Внутренний сервисный ключ для вызовов между канал-адаптером (бот) и
    бэкендом — не для конечных пользователей сайта. В отличие от
    TELEGRAM_BOT_TOKEN/ANTHROPIC_API_KEY (пустое значение просто выключает
    функцию), здесь пустой ASSISTANT_API_KEY означает «доступ закрыт для
    всех» (fail closed) — эндпоинт дёргает платный Claude API и пишет в БД,
    открывать его по умолчанию нельзя."""
    message = 'Неверный или отсутствующий заголовок X-Assistant-Key.'

    def has_permission(self, request, view):
        key = request.headers.get('X-Assistant-Key', '')
        return bool(settings.ASSISTANT_API_KEY) and key == settings.ASSISTANT_API_KEY
