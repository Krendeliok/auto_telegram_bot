from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InputMediaPhoto, MediaGroup

from ..contexts import FSMNews

from ..queries.client import (
    is_admin,
    is_owner,
    get_user_phone,
    can_create_and_kind_adv,
)
from ..queries.advertisement import (
    get_random_admin,
    pin_admin,
    get_advertisement_by_id,
    is_spam,
)
from ..queries.create import (
    create_advertisement,
)

from ..keyboards import (
    producers_keyboard, 
    models_keyboard,
    engine_keyboard,
    gearbox_keyboard,
    country_keyboard,
    adverisement_keyboard,
    commands_keyboard,
    back_complete_keyboard,
    phone_numbers_keyboard,
)
from datetime import date
from ..texts import RULES

from config import MAX_IMAGES

from ..commands import general, special
from .general import start_command


async def start_news(message: types.Message, state: FSMContext):
    await FSMNews.text.set()
    await message.answer("Введіть текст вашої новини", reply_markup=back_complete_keyboard(deny=True))


async def cancel_handler(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return
    await state.finish()
    await message.reply("Скасовано!", reply_markup=commands_keyboard(message.from_user.id))


def back_handler(previous_func, key=None):
    def wrapper(func):
        async def inner(message, state, *args, **kwargs):
            if message.text == special["back"]:
                if key is not None:
                    async with state.proxy() as data:
                        message.text = data[key]
                await previous_func(message=message, state=state)
                return
            await func(message=message, state=state)
        return inner
    return wrapper


@back_handler(previous_func=start_command)
async def set_text(message: types.Message, state: FSMContext):
    await state.set_state(FSMNews.photo)
    await state.update_data({"text": message.text})
    await message.answer("Відправте зображення для новини", reply_markup=back_complete_keyboard(deny=True))


@back_handler(previous_func=start_news, key="text")
async def set_images(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data["image_counter"] = 1
            data["images"] = [message.photo[0].file_id]
        await state.set_state(FSMNews.more_images)


@back_handler(previous_func=start_news, key="text")
async def more_images(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data["image_counter"] < int(MAX_IMAGES):
            data["image_counter"] += 1
            data["images"].append(message.photo[0].file_id)
        else:
            await message.answer(f"🟠Фотографій вже забагато, я залишу тільки перші {MAX_IMAGES}", reply_markup=back_complete_keyboard(deny=True, complete=True))


def register_handlers_news(dp: Dispatcher):
    dp.register_message_handler(start_news, Text(equals=special["create_news"], ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=special["end"])
    dp.register_message_handler(cancel_handler, Text(equals=special["end"], ignore_case=True), state="*")