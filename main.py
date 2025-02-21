import asyncio
import logging

from aiogram import types
from aiogram.filters.command import Command

from bot import bot, dp

import chat
import comment

logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    print(message)
    await message.answer(str(message.from_user.id))

@dp.message()
async def chitchat(message: types.Message):

    if message.chat.id != -1002261267865:
        await message.reply("Тут я не отвечаю. Я работаю только в комментариях этого канала: @gleb_vedaet")
        return

    if message.is_automatic_forward and message.video is not None:
        await comment.video(message)
    elif message.is_automatic_forward and message.photo is not None:
        print('get photo')
        await comment.photo(message)
    elif message.is_automatic_forward and message.text is not None:
        await comment.text(message)

    elif message.reply_to_message.from_user.id == bot.id or \
        (message.text is not None and "гыча" in message.text.lower()) or \
            (message.text is not None and "@my_gycha_bot" in message.text.lower()):
        if message.video is not None:
            await comment.video(message, from_user=True)
        elif message.photo is not None:
            await comment.photo(message, from_user=True)
        elif message.text is not None:
            try:
                answer = await chat.get_response(message.text, message.from_user.username)
            except Exception as e:
                logging.error(e)
                answer = "Я хотел ответить на этот вопрос, но мне отрезали нос и я расхотел."
                chat.add_message("", "assistant", answer)
            await message.answer(
                answer,
                parse_mode="Markdown",
                reply_to_message_id=message.message_id,
            )
        else:
            await message.answer(
                "Извини, я ещё не умею работать с контентом такого рода. Я распознаю только текст, картинки и видео.",
                parse_mode="Markdown",
                reply_to_message_id=message.message_id,
            )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())