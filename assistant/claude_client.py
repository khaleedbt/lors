import anthropic
from django.conf import settings

from . import ai_tools

MODEL = 'claude-opus-4-8'
MAX_TOOL_ROUNDS = 3


def _client():
    if settings.ANTHROPIC_API_KEY:
        return anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return anthropic.Anthropic()  # falls back to the SDK's own credential resolution


def _tools():
    """ai_tools.TOOL_DEFS в формате Anthropic — тот же JSON Schema, только
    под ключом input_schema вместо parameters. cache_control на последнем
    инструменте кэширует весь блок tools целиком (Anthropic кэширует всё
    до точки останова включительно) — вместе с system это убирает System
    и Tools из стоимости каждого повторного запроса (см. system ниже)."""
    tools = [
        {'name': t['name'], 'description': t['description'], 'input_schema': t['parameters']}
        for t in ai_tools.TOOL_DEFS
    ]
    if tools:
        tools[-1] = {**tools[-1], 'cache_control': {'type': 'ephemeral'}}
    return tools


def ask_claude(user_text: str, history: list[dict] | None = None) -> str:
    client = _client()
    messages = (history or []) + [{'role': 'user', 'content': user_text}]

    # System и tools вычисляются один раз на вызов (не на каждый из до 3
    # раундов tool-use) и кэшируются на стороне Anthropic (cache_control) —
    # System не меняется внутри одного ask_claude(), а между вызовами
    # meняется редко (правки в /admin/), так что кэш почти всегда попадает.
    # TTL кэша — 5 минут, этого достаточно на весь раунд tool-use и обычно
    # на следующее сообщение того же клиента.
    system = [{'type': 'text', 'text': ai_tools.system_prompt(), 'cache_control': {'type': 'ephemeral'}}]
    tools = _tools()

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason != 'tool_use':
            return next((b.text for b in response.content if b.type == 'text'), '')

        messages.append({'role': 'assistant', 'content': response.content})
        tool_results = [
            {
                'type': 'tool_result',
                'tool_use_id': block.id,
                'content': ai_tools.TOOL_HANDLERS[block.name](block.input),
            }
            for block in response.content if block.type == 'tool_use'
        ]
        messages.append({'role': 'user', 'content': tool_results})

    return 'Извини, не получилось обработать запрос — напиши нам напрямую.'
