from .claude_client import ask_claude
from .models import BotMessage

HISTORY_LIMIT = 20  # last N messages (≈10 exchanges) kept as context for a reply

ROLE_BY_DIRECTION = {
    BotMessage.DIRECTION_IN: 'user',
    BotMessage.DIRECTION_OUT: 'assistant',
}


def _recent_history(channel: str, external_user_id: str) -> list[dict]:
    recent = BotMessage.objects.filter(
        channel=channel, external_user_id=external_user_id,
    ).order_by('-created_at')[:HISTORY_LIMIT]
    return [
        {'role': ROLE_BY_DIRECTION[m.direction], 'content': m.text}
        for m in reversed(recent)
    ]


def handle_message(text: str, *, channel: str, external_user_id: str) -> str:
    """Channel-agnostic entry point — Telegram today, other channels later
    (e.g. Instagram) call this same function with their own adapter."""
    history = _recent_history(channel, external_user_id)

    BotMessage.objects.create(
        channel=channel, external_user_id=external_user_id,
        direction=BotMessage.DIRECTION_IN, text=text,
    )

    reply = ask_claude(text, history=history)

    BotMessage.objects.create(
        channel=channel, external_user_id=external_user_id,
        direction=BotMessage.DIRECTION_OUT, text=reply,
    )
    return reply
