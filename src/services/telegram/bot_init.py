import os
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)