from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .brain import handle_message
from .permissions import HasAssistantKey
from .serializers import AssistantMessageRequestSerializer, AssistantMessageResponseSerializer


class AssistantMessageView(APIView):
    """Единая точка входа для ассистента, канал-агностичная: любой
    канал-адаптер (Telegram сейчас, Instagram/WhatsApp/веб-виджет позже)
    шлёт сюда {channel, external_user_id, text} и получает {reply}.

    Вся логика ответа — история переписки, вызов Claude, лог в BotMessage —
    остаётся на бэкенде (assistant/brain.py); адаптер ничего не генерирует
    сам, только пересылает сообщение сюда и относит reply дальше через свой
    SDK канала (Telegram Bot API, Meta Graph API и т.п.). См. runbot.py —
    он теперь именно такой тонкий HTTP-клиент, а не прямой Python-вызов.

    Закрыт заголовком X-Assistant-Key (см. permissions.HasAssistantKey) —
    это внутренний сервисный вызов, не публичный эндпоинт."""
    permission_classes = [HasAssistantKey]

    @extend_schema(request=AssistantMessageRequestSerializer, responses=AssistantMessageResponseSerializer)
    def post(self, request):
        req = AssistantMessageRequestSerializer(data=request.data)
        req.is_valid(raise_exception=True)

        reply = handle_message(
            req.validated_data['text'],
            channel=req.validated_data['channel'],
            external_user_id=req.validated_data['external_user_id'],
        )
        data = AssistantMessageResponseSerializer({'reply': reply}).data
        return Response(data, status=status.HTTP_200_OK)
