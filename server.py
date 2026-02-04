import os
from openai import OpenAI
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Клиент DeepSeek
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

async def ask_deepseek(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я CodeTutorDevBot. Напиши мне вопрос.")

@dp.message()
async def handle_message(message: types.Message):
    reply = await asyncio.to_thread(ask_deepseek, message.text)
    await message.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())