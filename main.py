import asyncio
import logging
from platform import system

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import config
import chat
import ocr

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TG_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(str(message.from_user.id))

@dp.message()
async def chitchat(message: types.Message):
    # if message.chat.id != -1002261267865:
    #     await message.answer("Тут я не отвечаю. Я работаю только в комментариях этого канала: @gleb_vedaet")
    #     return

    if message.video is not None:
        data = await bot.get_file(message.video.thumbnail.file_id)
        url = f"https://api.telegram.org/file/bot{config.TG_TOKEN}/{data.file_path}"
        text = await ocr.get(url)
        if len(text) == 0:
            text = "В канале опубликовано видео."
        else:
            text = "В канале опубликован видео с таким текстом:" + text
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
        return
    elif message.photo is not None:
        data = await bot.get_file(message.photo[-1].file_id)
        url = f"https://api.telegram.org/file/bot{config.TG_TOKEN}/{data.file_path}"
        text = await ocr.get(url)
        if len(text) == 0:
            text = "В канале опубликован мем без текста или с нераспознанным текстом."
        else:
            text = "В канале опубликован мем с таким текстом:" + text
        try:
            answer = await chat.get_response(text,"System")
        except Exception as e:
            logging.error(e)
            answer = "Я хотел прокоментировать этот пост, но мне отрезали нос и я расхотел."
        print(answer)
        await message.answer(
            answer,
            parse_mode="Markdown",
            reply_to_message_id=message.message_id
        )
        return

    try:
        answer = await chat.get_response(message.text, message.from_user.username)
    except Exception as e:
        logging.error(e)
        answer = "Я хотел ответить на этот вопрос, но мне отрезали нос и я расхотел."
    await message.answer(
        answer,
        parse_mode="Markdown",
        reply_to_message_id=message.message_id,
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())