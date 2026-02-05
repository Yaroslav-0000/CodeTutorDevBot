import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TRAIN_PASSWORD = os.environ.get("TRAIN_PASSWORD", "1234")  # пароль по умолчанию

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("""
Привет, я бот созданный для обучения программированию, вот что вам я предложу:

написать текст /exemple_print
""")

@dp.message(Command("exemple_print"))
async def cmd_exemple_print(message: types.Message)
    await message.answer('"print("text")"')

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text.strip()

    if message.from_user.id not in authorized_users:
        await message.answer("⛔ Ты не вошёл под паролем. Используй /login <пароль>.")
        return

    # Если сообщение начинается с "Ответ:", учим ИИ
    if user_text.lower().startswith("ответ:"):
        if "last_question" in knowledge:
            answer = user_text[6:].strip()
            knowledge[knowledge["last_question"]] = answer
            await message.answer("✅ Я запомнил новый ответ.")
        else:
            await message.answer("❌ Сначала задай вопрос, потом дай 'Ответ: ...'.")
    else:
        # Сохраняем вопрос как последний
        knowledge["last_question"] = user_text
        reply = generate_reply(user_text)
        await message.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())