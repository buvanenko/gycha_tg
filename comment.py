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
        answer = "Я хотел прокоментировать это, но мне отрезали нос и я расхотел."

    await message.answer(
        answer,
        parse_mode="Markdown",
        reply_to_message_id=message.message_id
    )

async def video(message: Message, from_user = False):
    data = await bot.get_file(message.video.thumbnail.file_id)
    url = f"https://api.telegram.org/file/bot{config.TG_TOKEN}/{data.file_path}"
    try:
        text = await vision.get(url)
        if from_user:
            text = f"Пользователь [{message.from_user.username}] оставил видео в качестве комментария. Словесное описание кадра: {text}. "
        else:
            text = "В канале опубликовано видео. Словесное описание кадра: " + text + '. '
    except Exception as e:
        logging.error(e)
        if from_user:
             text = f"Пользователь [{message.from_user.username}] оставил видео в качестве комментария."
        else:
            text = "В канале опубликовано видео. "
    text_ocr = await ocr.get(url)
    text += 'Распознанный текст из кадра: ' + text_ocr + '. '

    if message.text is not None:
        if from_user:
            text += 'Текст комментария: ' + message.text
        else:
            text += 'Текст поста: ' + message.text

    await send(message, text)


async def photo(message: Message, from_user = False):
    data = await bot.get_file(message.photo[-1].file_id)
    url = f"https://api.telegram.org/file/bot{config.TG_TOKEN}/{data.file_path}"
    print(url)
    try:
        text = await vision.get(url)
        if from_user:
            text = f"Пользователь [{message.from_user.username}] оставил изображение в качестве комментария. Словесное описание: {text}. "
        else:
            text = "В канале опубликован мем. Словесное описание: " + text + '. '
    except Exception as e:
        logging.error(e)
        if from_user:
            text = f"Пользователь [{message.from_user.username}] оставил изображение в качестве комментария."
        else:
            text = "В канале опубликован мем. "

    text_ocr = await ocr.get(url)
    text += 'Распознанный текст на изображении: ' + text_ocr + '. '

    if message.text is not None:
        if from_user:
            text += 'Текст комментария: ' + message.text
        else:
            text += 'Текст поста: ' + message.text
    print(text)
    await send(message, text)

async def text(message: Message):
    await send(message, "В канале опубликован пост: " + message.text)