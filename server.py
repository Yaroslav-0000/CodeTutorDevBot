from transformers import pipeline
from aiogram import Bot, Dispatcher, types
import asyncio, os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Загружаем локальную модель (например, GPT-2 small)
generator = pipeline("text-generation", model="gpt2")

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text
    reply = generator(user_text, max_length=50, num_return_sequences=1)[0]["generated_text"]
    await message.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())