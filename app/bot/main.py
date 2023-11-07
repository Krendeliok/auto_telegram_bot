import logging
from src.disp import create_dispatcher
from src.session import create_session
from aiogram import Bot, executor

from sqlalchemy import create_engine
from config import DATABASE_URI, API_TOKEN, CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

from models import Base

from aiogram.contrib.fsm_storage.memory import MemoryStorage

import cloudinary

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=API_TOKEN, parse_mode='html')
dp = create_dispatcher(bot, storage=storage)

engine = create_engine(DATABASE_URI)
Base.metadata.bind = engine

session = create_session(engine)

from src.bot import *

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
