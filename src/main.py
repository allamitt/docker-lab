import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from settings import BOT_TOKEN
from ai import ai_request


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!" +
                          "Я бот искуственного готовый помочь с любыми вопросами или просто поболтать." +
                          "Чем могу помочь сегодня?")


@dp.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer(f'/new для сброса контекста общения с моделью ')


@dp.message(Command('new'))
async def new_context(message: Message):
    await message.answer('Диалог успешно сброшен')


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        response = await ai_request(user_input=message.text, user_id=message.from_user.id)
        await message.answer(response)
    except Exception as e:
        logging.error(f'an exception in handling AI requests: {e}')
        await message.answer('Упс... Что-то пошло не по плану.. Попробуйте позже')


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
