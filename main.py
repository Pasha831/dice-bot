import asyncio
import logging
import os
from asyncio import sleep

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


def get_keyboard():
    kb = [
            [
                types.KeyboardButton(text="1️⃣"),
                types.KeyboardButton(text="2️⃣"),
                types.KeyboardButton(text="3️⃣"),
                types.KeyboardButton(text="4️⃣"),
                types.KeyboardButton(text="5️⃣"),
                types.KeyboardButton(text="6️⃣"),
            ],
        ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("🧐 Guess a number on a dice 🎲", reply_markup=get_keyboard())


@dp.message_handler(state="*")
async def message_handler(message: types.Message):
    emoji_to_digit = {"1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4, "5️⃣": 5, "6️⃣": 6}

    if message.text in emoji_to_digit:
        msg = await bot.send_dice(chat_id=message.chat.id)

        await sleep(4)

        if emoji_to_digit[message.text] == msg.dice.value:
            await bot.send_message(chat_id=message.chat.id, text="🎉 You're a lucky one!")
        else:
            await bot.send_message(chat_id=message.chat.id, text="😢 Not this time, try again!")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
