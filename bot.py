from aiogram import Bot, Dispatcher
from config import config

bot = Bot(token=config.telegram.token)
dp = Dispatcher()