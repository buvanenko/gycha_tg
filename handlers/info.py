from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("info"))
async def info(message: Message):
    answer = f"message.chat.id: {message.chat.id}\n"
    answer += f"message.chat.type: {message.chat.type}\n"
    answer += f"message.from_user.id: {message.from_user.id}"
    await message.reply(answer)