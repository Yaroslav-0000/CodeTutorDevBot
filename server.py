import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("""
Привет, я бот созданный для обучения программированию, вот что вам я предложу:

написать текст /exemple_print
""")

@dp.message(Command("exemple_print"))
async def cmd_exemple_print(message: types.Message):
    await message.answer(
        "```python\nprint('Hello, world!')\n```",
        parse_mode="MarkdownV2"
    )

@dp.message()
async def handle_message(message: types.Message):
    await message.answer("")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())