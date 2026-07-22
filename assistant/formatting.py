import html
import re


def markdown_to_telegram_html(text: str) -> str:
    """Claude отвечает обычным Markdown (**bold**, *italic*, `code`).
    Telegram не парсит его сам — переводим в HTML-подмножество, которое
    понимает Bot API (parse_mode='HTML'), с экранированием остального текста."""
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', escaped)
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', escaped)
    escaped = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', escaped)
    escaped = re.sub(r'`([^`]+?)`', r'<code>\1</code>', escaped)
    return escaped
