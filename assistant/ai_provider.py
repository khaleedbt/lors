"""
Переключатель активного провайдера ИИ — AssistantSettings.provider (БД,
редактируется в /admin/, см. assistant/models.py), не .env: меняется без
рестарта процесса, действует со следующего же запроса. Один активный
провайдер за раз, без автоматического fallback между ними.

Ключи провайдеров (ANTHROPIC_API_KEY и т.д.) остаются секретами в .env —
здесь только выбор, каким из уже настроенных провайдеров пользоваться.

Импорт клиента — внутри функции, а не на уровне модуля: не выбранный
сейчас провайдер (его SDK/ключ) вообще не трогается процессом.
"""

from .models import AssistantSettings


def ask_ai(user_text: str, history: list[dict] | None = None) -> str:
    provider = AssistantSettings.load().provider

    if provider == AssistantSettings.PROVIDER_OPENAI:
        from .openai_client import ask_openai
        return ask_openai(user_text, history=history)

    if provider == AssistantSettings.PROVIDER_DEEPSEEK:
        from .deepseek_client import ask_deepseek
        return ask_deepseek(user_text, history=history)

    from .claude_client import ask_claude
    return ask_claude(user_text, history=history)
