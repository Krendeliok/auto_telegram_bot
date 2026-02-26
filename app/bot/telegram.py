import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN

logger = logging.getLogger(__name__)


storage = MemoryStorage()

bot = Bot(token=API_TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=storage)

@dp.errors_handler()
async def errors_handler(update, exception):
    logger.exception("Update caused error: %r", exception)

    return True
