from django.db import models


class AssistantSettings(models.Model):
    """Синглтон — какой провайдер ИИ сейчас отвечает на /api/assistant/message/
    (см. assistant/ai_provider.py). Переключается из админки, без правки .env
    и без рестарта — ai_provider.py читает это значение из БД на каждый
    запрос. Ключи (ANTHROPIC_API_KEY и т.д.) остаются секретами в .env —
    здесь только выбор, каким из уже настроенных провайдеров пользоваться."""
    PROVIDER_CLAUDE = 'claude'
    PROVIDER_OPENAI = 'openai'
    PROVIDER_DEEPSEEK = 'deepseek'
    PROVIDER_CHOICES = [
        (PROVIDER_CLAUDE, 'Claude (Anthropic)'),
        (PROVIDER_OPENAI, 'OpenAI'),
        (PROVIDER_DEEPSEEK, 'DeepSeek'),
    ]

    provider = models.CharField('провайдер ИИ', max_length=20, choices=PROVIDER_CHOICES, default=PROVIDER_CLAUDE)

    class Meta:
        verbose_name = 'настройки ассистента'
        verbose_name_plural = 'настройки ассистента'

    def __str__(self):
        return f'Настройки ассистента ({self.get_provider_display()})'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


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
