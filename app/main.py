import logging
from src.disp import create_dispatcher
from src.session import create_session
from aiogram import Bot, executor

from sqlalchemy import create_engine
from config import DATABASE_URI, API_TOKEN

from models import Base

from aiogram.contrib.fsm_storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = create_dispatcher(bot, storage=storage)

engine = create_engine(DATABASE_URI)
Base.metadata.bind = engine

session = create_session(engine)

from src.bot import *

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
