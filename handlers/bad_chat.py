from aiogram import Router, F
from aiogram.types import Message

from config import config

router = Router()

@router.message(F.chat.id != config.telegram.chat_id)
async def info(message: Message):
    await message.reply("Тут я не отвечаю. Я работаю только в комментариях этого канала: @gleb_vedaet")