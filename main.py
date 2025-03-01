import asyncio
import logging
import chat
from handlers import info, bad_chat, photo, video, text
from bot import bot, dp

logging.basicConfig(level=logging.INFO)

async def on_startup(dispatcher):
    chat.load()
async def on_shutdown(dispatcher):
    chat.save()

async def main():

    dp.include_routers(
        info.router,
        bad_chat.router,
        photo.router, 
        video.router,
        text.router
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())