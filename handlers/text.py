from utils import chat
import logging
from bot import bot
from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text)
async def text(message: Message):

    if message.message_thread_id is None:
        thread_id = message.message_id
    else:
        thread_id = message.message_thread_id

    try:
        if message.is_automatic_forward:
            answer = await chat.get("System", "В канале опубликован пост: " + message.text, thread_id)
        elif (message.reply_to_message and message.reply_to_message.from_user.id == bot.id) or \
            (message.text is not None and "гыча" in message.text.lower()) or \
                (message.text is not None and "@my_gycha_bot" in message.text.lower()):
            answer = await chat.get(message.from_user.username, message.text, thread_id)
        else:
            return
    except Exception as e:
        logging.error(e)
        answer = "Я хотел прокоментировать этот пост, но мне отрезали нос и я расхотел."
    await message.reply(answer, parse_mode="Markdown")