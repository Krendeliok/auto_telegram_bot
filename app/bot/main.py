import logging
from aiogram import executor
from telegram import dp

from config import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
)


import cloudinary


cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

logging.basicConfig(level=logging.INFO)

from src.handlers import *

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
