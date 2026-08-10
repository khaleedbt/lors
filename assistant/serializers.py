from rest_framework import serializers

from .models import BotMessage


class AssistantMessageRequestSerializer(serializers.Serializer):
    channel = serializers.ChoiceField(choices=BotMessage.CHANNEL_CHOICES)
    external_user_id = serializers.CharField(max_length=100)
    text = serializers.CharField(allow_blank=True)


class AssistantMessageResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()
