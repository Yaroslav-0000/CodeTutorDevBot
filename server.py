import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher, types

# 🔑 Берём токены из переменных окружения
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Функция запроса к DeepSeek API
async def ask_deepseek(prompt: str) -> str:
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]

# Обработчик сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    ai_reply = await ask_deepseek(user_text)
    await message.answer(ai_reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
