import json

from django.conf import settings
from openai import OpenAI

from . import ai_tools

# DeepSeek API — OpenAI-совместимый (chat.completions), просто другой
# base_url/ключ и классический формат tool_calls (не Responses API, как у
# openai_client.py). deepseek-v4-flash — самый дешёвый тир, для простого
# tool-calling/шаблонных ответов консультанта этого достаточно;
# deepseek-v4-pro доступен, если понадобится качество выше.
MODEL = 'deepseek-v4-flash'
BASE_URL = 'https://api.deepseek.com'
MAX_TOOL_ROUNDS = 3


def _client():
    return OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url=BASE_URL)


def _tools():
    """ai_tools.TOOL_DEFS в формате OpenAI Chat Completions —
    {"type": "function", "function": {name, description, parameters}},
    отличается от openai_client.py (Responses API), где те же поля лежат
    плоско без вложенного "function"."""
    return [
        {'type': 'function', 'function': {'name': t['name'], 'description': t['description'], 'parameters': t['parameters']}}
        for t in ai_tools.TOOL_DEFS
    ]


def ask_deepseek(user_text: str, history: list[dict] | None = None) -> str:
    client = _client()
    messages = [{'role': 'system', 'content': ai_tools.system_prompt()}] + (history or []) + [
        {'role': 'user', 'content': user_text},
    ]
    # tools — один раз на вызов, не на каждый раунд (то же соображение, что
    # в openai_client.py: DeepSeek тоже кэширует повторяющийся префикс
    # автоматически, только если он не меняется между запросами).
    tools = _tools()

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content or ''

        messages.append(message)
        for call in message.tool_calls:
            args = json.loads(call.function.arguments) if call.function.arguments else {}
            result = ai_tools.TOOL_HANDLERS[call.function.name](args)
            messages.append({'role': 'tool', 'tool_call_id': call.id, 'content': result})

    return 'Извини, не получилось обработать запрос — напиши нам напрямую.'
