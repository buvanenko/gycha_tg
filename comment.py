import logging
from aiogram.types import Message
from bot import bot

import vision
import ocr
import config
import chat

async def send(message: Message, text: str):
    try:
        answer = await chat.get_response(text,"System")
    except Exception as e:
        logging.error(e)
        answer = "Я хотел прокоментировать этот пост, но мне отрезали нос и я расхотел."

    await message.answer(
        answer,
        parse_mode="Markdown",
        reply_to_message_id=message.message_id
    )

async def video(message: Message):
    data = await bot.get_file(message.video.thumbnail.file_id)
    url = f"https://api.telegram.org/file/bot{config.TG_TOKEN}/{data.file_path}"
    try:
        text = await vision.get(url)
        text = "В канале опубликовано видео. Словесное описание кадра: " + text + '. '
    except Exception as e:
        logging.error(e)
        text = "В канале опубликовано видео. "
    text_ocr = await ocr.get(url)
    text += 'Распознанный текст из кадра: ' + text_ocr + '. '

    if message.text is not None:
        text += 'Текст поста: ' + message.text

    await send(message, text)


async def photo(message: Message):
    data = await bot.get_file(message.photo[-1].file_id)
    url = f"https://api.telegram.org/file/bot{config.TG_TOKEN}/{data.file_path}"

    try:
        text = await vision.get(url)
        text = "В канале опубликован мем. Словесное описание: " + text + '. '
    except Exception as e:
        logging.error(e)
        text = "В канале опубликован мем. "

    text_ocr = await ocr.get(url)
    text += 'Распознанный текст на изображении: ' + text_ocr + '. '

    if message.text is not None:
        text += 'Текст поста: ' + message.text

    await send(message, text)

async def text(message: Message):
    await send(message, "В канале опубликован пост: " + message.text)