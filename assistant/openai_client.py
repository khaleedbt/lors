import json

from django.conf import settings
from openai import OpenAI

from . import ai_tools

MODEL = 'gpt-6-astra'
MAX_TOOL_ROUNDS = 3


def _client():
    if settings.OPENAI_API_KEY:
        return OpenAI(api_key=settings.OPENAI_API_KEY)
    return OpenAI()  # falls back to the SDK's own credential resolution


def _tools():
    """ai_tools.TOOL_DEFS в формате OpenAI Responses API — тот же JSON
    Schema, только под ключом parameters с плоской обёрткой type:'function'
    (вместо вложенного input_schema, как у Anthropic)."""
    return [
        {'type': 'function', 'name': t['name'], 'description': t['description'], 'parameters': t['parameters']}
        for t in ai_tools.TOOL_DEFS
    ]


def ask_openai(user_text: str, history: list[dict] | None = None) -> str:
    client = _client()
    # history — уже {role, content} пары из BotMessage (brain.py), этот же
    # плоский формат Responses API принимает как есть, без конвертации.
    input_list = (history or []) + [{'role': 'user', 'content': user_text}]

    # instructions/tools — один раз на вызов, не на каждый из до 3 раундов:
    # OpenAI кэширует повторяющийся префикс запроса автоматически (без
    # cache_control, в отличие от Anthropic), но только если он побайтово
    # совпадает между запросами — пересчитывать заново на каждом раунде
    # рисковало бы разъехаться (правка в /admin/ между раундами) и сорвать
    # кэш-хит впустую.
    instructions = ai_tools.system_prompt()
    tools = _tools()

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.responses.create(
            model=MODEL,
            instructions=instructions,
            tools=tools,
            input=input_list,
        )

        function_calls = [item for item in response.output if item.type == 'function_call']
        if not function_calls:
            return response.output_text

        input_list += response.output
        for item in function_calls:
            args = json.loads(item.arguments) if item.arguments else {}
            result = ai_tools.TOOL_HANDLERS[item.name](args)
            input_list.append({'type': 'function_call_output', 'call_id': item.call_id, 'output': result})

    return 'Извини, не получилось обработать запрос — напиши нам напрямую.'
