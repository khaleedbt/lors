import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from assistant.brain import handle_message
from assistant.formatting import markdown_to_telegram_html


async def _main(token: str) -> None:
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message) -> None:
        await message.answer(
            'Здравствуйте! Напишите марку и модель автомобиля — подскажу, '
            'есть ли для неё коврик по лекалу.',
        )

    @dp.message()
    async def on_message(message: Message) -> None:
        reply = await sync_to_async(handle_message)(
            message.text or '', channel='telegram', external_user_id=str(message.from_user.id),
        )
        await message.answer(markdown_to_telegram_html(reply))

    await dp.start_polling(bot)


class Command(BaseCommand):
    help = 'Запустить Telegram-бота (aiogram, long polling)'

    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            raise CommandError('TELEGRAM_BOT_TOKEN не задан в .env')
        asyncio.run(_main(settings.TELEGRAM_BOT_TOKEN))
