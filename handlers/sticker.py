from utils import chat, visual
import logging
from aiogram import Router, F
from aiogram.types import Message
from bot import bot
from config import config

router = Router()

@router.message(F.sticker)
async def sticker(message: Message):

    if message.message_thread_id is None:
        thread_id = message.message_id
    else:
        thread_id = message.message_thread_id

    if message.is_automatic_forward:
        text = "В канале опубликован новый пост со стикером."
    elif (message.reply_to_message and message.reply_to_message.from_user.id == bot.id):
        text = f"Пользователь [{message.from_user.username}] оставил стикер в качестве комментария."
    else:
        return
    
    data = await bot.get_file(message.sticker.thumbnail.file_id)
    url = f"https://api.telegram.org/file/bot{config.telegram.token}/{data.file_path}"

    visual_description = await visual.get(url)
    if visual_description is not None:
        text = f"{text}\n\nОписание стикера: {visual_description}"

    if message.sticker.emoji is not None:
        text = f"{text}\n\nСмайлик стикера: {message.sticker.emoji}"

    logging.info(text)

    try:
        answer = await chat.get("System", text, thread_id)
    except Exception as e:
        logging.error(e)
        answer = "Я хотел прокоментировать этот стикер, но мне отрезали нос и я расхотел."
    await message.reply(answer, parse_mode="Markdown")