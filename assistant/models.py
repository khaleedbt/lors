from django.db import models


class BotMessage(models.Model):
    CHANNEL_TELEGRAM = 'telegram'
    CHANNEL_CHOICES = [
        (CHANNEL_TELEGRAM, 'Telegram'),
    ]

    DIRECTION_IN = 'in'
    DIRECTION_OUT = 'out'
    DIRECTION_CHOICES = [
        (DIRECTION_IN, 'от клиента'),
        (DIRECTION_OUT, 'от бота'),
    ]

    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    external_user_id = models.CharField('id пользователя в канале', max_length=100)
    direction = models.CharField(max_length=3, choices=DIRECTION_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'сообщение бота'
        verbose_name_plural = 'сообщения бота'

    def __str__(self):
        return f'{self.channel}:{self.external_user_id} [{self.direction}]'
