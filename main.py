import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="🏀"),
            types.KeyboardButton(text="🎲"),
            types.KeyboardButton(text="help me!")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer("Hello!", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    
