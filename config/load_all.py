import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


token = os.environ["TELEGRAM_BOT_TOKEN"]
bot = Bot(token, parse_mode="html")
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage,)