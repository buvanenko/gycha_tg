import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import config
import chat

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TG_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Абоба!")

@dp.message()
async def cmd_start(message: types.Message):
    try:
        answer = await chat.get_response(message.text, message.from_user.id)
    except Exception as e:
        logging.error(e)
        answer = "Я хотел ответить на этот вопрос, но мне отрезали нос и я расхотел."
    await message.answer(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())