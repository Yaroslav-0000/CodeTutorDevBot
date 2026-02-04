import os
import asyncio
import torch
import torch.nn as nn
import torch.optim as optim
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 🔑 токен бота из переменных окружения
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# --- Модель в оперативке ---
class TinyAI(nn.Module):
    def __init__(self, vocab_size=128, embed_dim=32, hidden_dim=64):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.GRU(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = self.embed(x)
        out, _ = self.rnn(x)
        return self.fc(out)

# создаём модель и оптимизатор (всё хранится в RAM)
vocab_size = 128
model = TinyAI(vocab_size)
optimizer = optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.CrossEntropyLoss()

# простая "память" обучения — список пар (вопрос, ответ)
training_data = []

# функция обучения на лету
def train_step(input_ids, target_ids):
    model.train()
    optimizer.zero_grad()
    out = model(input_ids)
    loss = loss_fn(out.view(-1, vocab_size), target_ids.view(-1))
    loss.backward()
    optimizer.step()
    return loss.item()

# генерация ответа (пока примитивная)
def generate_reply(text: str) -> str:
    # просто возвращаем echo + " (ИИ)"
    return f"{text} (ИИ)"

# --- Telegram бот ---
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я твой ИИ. Каждый запуск — чистая память.")

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text

    # добавляем в "память"
    training_data.append((user_text, "ответ"))

    # делаем шаг обучения (условно, на фейковых данных)
    input_ids = torch.randint(0, vocab_size, (1, 5))
    target_ids = torch.randint(0, vocab_size, (1, 5))
    loss = train_step(input_ids, target_ids)

    # генерируем ответ
    reply = generate_reply(user_text)
    await message.answer(f"{reply}\n[loss={loss:.4f}]")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())