import asyncio
import logging

import httpx
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from assistant.formatting import markdown_to_telegram_html

logger = logging.getLogger(__name__)

FALLBACK_REPLY = 'Извините, сейчас не получается ответить. Попробуйте чуть позже.'


async def _ask_backend(client: httpx.AsyncClient, *, channel: str, external_user_id: str, text: str) -> str:
    """Единственная точка связи с бэкендом — POST /api/assistant/message/.
    Бот сам ничего не генерирует, только пересылает сообщение и относит
    ответ дальше; при сетевой ошибке/таймауте отдаёт запасной текст, а не
    падает и не молчит."""
    try:
        r = await client.post(
            '/api/assistant/message/',
            json={'channel': channel, 'external_user_id': external_user_id, 'text': text},
            headers={'X-Assistant-Key': settings.ASSISTANT_API_KEY},
        )
        r.raise_for_status()
        return r.json()['reply']
    except httpx.HTTPError:
        logger.exception('assistant API: ошибка запроса')
        return FALLBACK_REPLY


async def _main(token: str) -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    async with httpx.AsyncClient(base_url=settings.BACKEND_BASE_URL, timeout=60) as client:
        @dp.message(CommandStart())
        async def start(message: Message) -> None:
            await message.answer(
                'Здравствуйте! Напишите марку и модель автомобиля — подскажу, '
                'есть ли для неё коврик по лекалу.',
            )

        @dp.message()
        async def on_message(message: Message) -> None:
            reply = await _ask_backend(
                client, channel='telegram', external_user_id=str(message.from_user.id), text=message.text or '',
            )
            await message.answer(markdown_to_telegram_html(reply))

        await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Запустить Telegram-бота (aiogram, long polling) — тонкий адаптер над /api/assistant/message/'

    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            raise CommandError('TELEGRAM_BOT_TOKEN не задан в .env')
        if not settings.ASSISTANT_API_KEY:
            raise CommandError('ASSISTANT_API_KEY не задан в .env — без него бэкенд не примет запрос от бота')
        asyncio.run(_main(settings.TELEGRAM_BOT_TOKEN))
