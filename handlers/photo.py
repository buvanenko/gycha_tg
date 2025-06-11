from utils import visual, chat
import logging
from aiogram import Router, F
from aiogram.types import Message
from bot import bot
from config import config

router = Router()

@router.message(F.photo)
async def photo(message: Message):

    if message.message_thread_id is None:
        thread_id = message.message_id
    else:
        thread_id = message.message_thread_id

    if message.is_automatic_forward:
        text = "В канале опубликован новый пост с изображением."
    elif (message.reply_to_message and message.reply_to_message.from_user.id == bot.id) or \
            (message.text is not None and "гыча" in message.text.lower()) or \
                (message.text is not None and "@my_gycha_bot" in message.text.lower()):
        text = f"Пользователь [{message.from_user.username}] оставил изображение в качестве комментария."
    else:
        return
    
    data = await bot.get_file(message.photo[-1].file_id)
    url = f"https://api.telegram.org/file/bot{config.telegram.token}/{data.file_path}"

    visual_description = await visual.get(url)
    if visual_description is not None:
        text = f"{text}\n\nОписание изображения: {visual_description}"

    if message.text is not None:
        text = f"{text}\n\nТекст в сообщении: {message.text}"

    logging.info(text)

    try:
        answer = await chat.get("System", text, thread_id)
    except Exception as e:
        logging.error(e)
        answer = "Я хотел прокоментировать это изображение, но мне отрезали нос и я расхотел."
    await message.reply(answer, parse_mode="Markdown")