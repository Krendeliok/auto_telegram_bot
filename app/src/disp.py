from aiogram import Dispatcher

current_dispatcher = None


def create_dispatcher(bot, storage=None):
    global current_dispatcher
    current_dispatcher = Dispatcher(bot, storage=storage)
    return current_dispatcher
