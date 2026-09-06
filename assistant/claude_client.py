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
    под ключом input_schema вместо parameters."""
    return [
        {'name': t['name'], 'description': t['description'], 'input_schema': t['parameters']}
        for t in ai_tools.TOOL_DEFS
    ]


def ask_claude(user_text: str, history: list[dict] | None = None) -> str:
    client = _client()
    messages = (history or []) + [{'role': 'user', 'content': user_text}]

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=ai_tools.system_prompt(),
            tools=_tools(),
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
