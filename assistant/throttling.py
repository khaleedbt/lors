from rest_framework.throttling import SimpleRateThrottle


class ExternalUserRateThrottle(SimpleRateThrottle):
    """Все каналы делят один X-Assistant-Key (см. permissions.HasAssistantKey) —
    штатный AnonRateThrottle/UserRateThrottle считал бы весь трафик бота одним
    клиентом и либо резал легитимных пользователей друг о друга, либо (по
    request.user, тут его вообще нет) не работал бы совсем. Ограничиваем по
    (channel, external_user_id) из тела запроса — конкретному человеку в
    Telegram/будущих каналах, а не бэкенду в целом. Смысл — не спам как
    таковой (ключ секретный), а стоимость: каждый вызов дёргает платный
    Claude/OpenAI/DeepSeek, один навязчивый чат не должен разгонять счёт."""
    scope = 'assistant_message'

    def get_cache_key(self, request, view):
        external_user_id = request.data.get('external_user_id')
        if not external_user_id:
            return None  # невалидный запрос — пусть падает на сериализаторе, не здесь
        channel = request.data.get('channel', '?')
        ident = f'{channel}:{external_user_id}'
        return self.cache_format % {'scope': self.scope, 'ident': ident}
