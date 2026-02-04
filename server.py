import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TRAIN_PASSWORD = os.environ.get("TRAIN_PASSWORD")  # пароль для входа

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Память ИИ (только в RAM)
memory = {}
authorized_users = set()  # кто вошёл под паролем

def generate_reply(text: str) -> str:
    if "html" in text.lower():
        return "<html><body><h1>Hello World</h1></body></html>"
    elif "python" in text.lower():
        return "def hello():\n    print('Hello, world!')"
    elif text in memory:
        return f"Я помню: {memory[text]}"
    else:
        return f"Ты сказал: {text}. Я учусь и теперь знаю это."

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Чтобы учить меня, введи команду /login <пароль>.")

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
    user_text = message.text
    if message.from_user.id in authorized_users:
        # сохраняем в память
        memory[user_text] = f"ответ на '{user_text}'"
        reply = generate_reply(user_text)
        await message.answer(reply)
    else:
        await message.answer("⛔ Ты не вошёл под паролем. Используй /login <пароль>.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())