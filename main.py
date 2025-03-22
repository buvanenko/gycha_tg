import asyncio
import logging
import chat
from handlers import info, bad_chat, photo, sticker, video, text
from bot import bot, dp

logging.basicConfig(level=logging.INFO)


async def main():

    dp.include_routers(
        info.router,
        bad_chat.router,
        photo.router, 
        sticker.router, 
        video.router,
        text.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())