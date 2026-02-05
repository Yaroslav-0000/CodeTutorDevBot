import os
import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TRAIN_PASSWORD = os.environ.get("TRAIN_PASSWORD", "1234")  # пароль по умолчанию

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Память ИИ (только в RAM)
knowledge = {}          # словарь: вопрос → ответ
authorized_users = set()  # кто вошёл под паролем

def generate_reply(text: str) -> str:
    # Если вопрос уже изучен — отвечаем по памяти
    if text in knowledge:
        # Чтобы не повторять одно и то же — добавляем вариации
        variants = [
            f"Я помню: {knowledge[text]}",
            f"Ты меня учил: {knowledge[text]}",
            f"Ранее ты сказал, что {knowledge[text]}",
            f"Моё знание: {knowledge[text]}"
        ]
        return random.choice(variants)
    else:
        # Если не знаем — просим обучить
        return "Я не знаю ответа. Напиши: Ответ: <текст>, чтобы меня научить."

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой ИИ. Чтобы учить меня, введи /login <пароль>.")

@dp.message(Command("login"))
async def cmd_login(message: types.Message):
    args = message.text.split()
    if len(args) == 2 and args[1] == TRAIN_PASSWORD:
        authorized_users.add(message.from_user.id)
        await message.answer("✅ Пароль верный. Теперь ты можешь учить меня.")
    else:
        await message.answer("❌ Неверный пароль.")

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