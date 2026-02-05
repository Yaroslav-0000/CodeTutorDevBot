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
Я бот созданный для обучения программированию, вот что я вам могу предложу:

python⬇️
написать текст /exemple_python_print
──────────────
html⬇️
пример базового кода /exemple_html_exemple
""")

@dp.message(Command("exemple_python_print"))
async def cmd_exemple_python_print(message: types.Message):
    await message.answer(
        "```python\nprint('text')\n```",
        parse_mode="MarkdownV2"
    )

@dp.message(Command("exemple_html_exemple"))
async def cmd_exemple_html_exemple(message: types.Message):
    await message.answer(
    "```html\n<!DOCTYPE html>\n<html>\n<head>\n    <title>Пример</title>\n</head>\n<body>\n</body>\n</html>\n```",
    parse_mode="MarkdownV2"
)

@dp.message()
async def handle_message(message: types.Message):
    await message.answer("")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())