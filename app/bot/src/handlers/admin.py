from telegram import dp
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config import CHANNEL_NAME

from ..contexts import (FSMAdmin, FSMSolution)
from ..keyboards import producers_keyboard, commands_keyboard, hide_keyboard, back_complete_keyboard

from ..queries.create import (
    create_city, 
    create_engine_type, 
    create_gearbox,
    create_model, 
    create_producer,
)
from ..queries.exists import (
    exists_producer,
)
from ..queries.client import (
    is_admin,
)
from ..queries.advertisement import (
    get_advertisement_by_id,  
    update_adv_status
)

from .general import start_command
from ..utils import make_advertisement

from ..commands import admin, special


def back_handler(previous_func, text=None):
    def wrapper(func):
        async def inner(message, state, *args, **kwargs):
            if message.text == special["back"]:
                if text is not None:
                    message.text = text
                await previous_func(message=message, state=state)
                return
            await func(message=message, state=state)
        return inner
    return wrapper


async def submit_advertisement(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.bot.answer_callback_query(callback_query.id)
    status, adv_id = callback_query["data"].split(":")
    update_adv_status(int(adv_id), status == "approve")
    adv = await get_advertisement_by_id(int(adv_id))
    await callback_query.message.delete()
    if status == "approve":
        await send_to_channel(callback_query.message, adv)
        await callback_query.message.answer("Погоджено!")
        await callback_query.bot.send_message(
            adv["client_telegram_id"],
            "✅Ваше оголошення погоджено і буде виставлятися раз на місяць.",
            reply_markup=commands_keyboard(adv["client_telegram_id"])
        )
    elif status == "reject":
        await callback_query.message.answer("Відхилено!")
        await FSMSolution.message.set()
        await state.update_data(user_id=adv["client_telegram_id"])
        await callback_query.bot.send_message(callback_query.from_user.id, "Напишіть причину відмови.", reply_markup=hide_keyboard())

async def send_reject_message(message: types.Message, state: FSMContext):
    reject_message = message.text
    async with state.proxy() as data:
        await message.bot.send_message(
            data["user_id"], 
            f"⭕️Ваше оголошення відхилено. Причина: {reject_message}.",
            reply_markup=commands_keyboard(data["user_id"])
        )
    await state.finish()

async def send_to_channel(message, adv):
    media_group = make_advertisement(adv)
    await message.bot.send_media_group(
            CHANNEL_NAME,
            media=media_group
    )

async def admin_creation_start(message: types.Message):
    if is_admin(message.from_user.id):
        if message.text == admin["create_producer"]:
            await FSMAdmin.create_producer.set()
            await message.answer("Вкажіть ім'я нової марки.", reply_markup=back_complete_keyboard())
        elif message.text == admin["create_model"]:
            await FSMAdmin.create_model.set()
            await message.answer("Вкажіть ім'я нової моделі.", reply_markup=back_complete_keyboard())
        elif message.text == admin["create_city"]:
            await FSMAdmin.create_region.set()
            await message.answer("Вкажіть ім'я нової області.", reply_markup=back_complete_keyboard())
        elif message.text == admin["create_engine_type"]:
            await FSMAdmin.create_engine.set()
            await message.answer("Вкажіть ім'я нового типу палива.", reply_markup=back_complete_keyboard())
        elif message.text == admin["create_gearbox"]:
            await FSMAdmin.create_gearbox.set()
            await message.answer("Вкажіть ім'я нової коробки.", reply_markup=back_complete_keyboard())

@back_handler(previous_func=start_command)
async def admin_create_producer(message: types.Message, state: FSMContext):
    await state.finish()
    create_producer(message.text)
    await message.answer("Марка створена.", reply_markup=commands_keyboard(message.from_user.id))

@back_handler(previous_func=start_command)
async def admin_create_engine_type(message: types.Message, state: FSMContext):
    await state.finish()
    create_engine_type(message.text)
    await message.answer("Тип палива створений.", reply_markup=commands_keyboard(message.from_user.id))

@back_handler(previous_func=start_command)
async def admin_create_city(message: types.Message, state: FSMContext):
    await state.finish()
    create_city(message.text)
    await message.answer("Область створена.", reply_markup=commands_keyboard(message.from_user.id))

@back_handler(previous_func=start_command)
async def admin_create_gearbox(message: types.Message, state: FSMContext):
    await state.finish()
    create_gearbox(message.text)
    await message.answer("Коробка створена.", reply_markup=commands_keyboard(message.from_user.id))

@back_handler(previous_func=start_command)
async def admin_create_model_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await state.set_state(FSMAdmin.set_producer)
    await message.answer("Оберіть марку машини.", reply_markup=producers_keyboard(no_end=True))

@back_handler(previous_func=admin_creation_start, text=admin["create_model"])
async def admin_create_model(message: types.Message, state: FSMContext):
    exists, obj = exists_producer(message.text)
    if exists:
        async with state.proxy() as data:
            create_model(data["name"], obj.id)
        await message.answer("Модель створена.", reply_markup=commands_keyboard(message.from_user.id))
        await state.finish()
    else:
        await message.reply("❌Це не схоже на марку. Спробуйте обрати з доступних.", reply_markup=producers_keyboard(no_end=True))
    

def register_handlers_admin(dp: Dispatcher):
    dp.register_callback_query_handler(
        submit_advertisement, 
        lambda c: c.data.startswith("approve") or c.data.startswith("reject"), 
        state="*"
    )
    dp.register_message_handler(send_reject_message, state=FSMSolution.message)
    dp.register_message_handler(admin_creation_start, Text(equals=admin.values(), ignore_case=True), state=None)
    dp.register_message_handler(admin_create_producer, state=FSMAdmin.create_producer)
    dp.register_message_handler(admin_create_model_name, state=FSMAdmin.create_model)
    dp.register_message_handler(admin_create_model, state=FSMAdmin.set_producer)
    dp.register_message_handler(admin_create_engine_type, state=FSMAdmin.create_engine)
    dp.register_message_handler(admin_create_gearbox, state=FSMAdmin.create_gearbox)
    dp.register_message_handler(admin_create_city, state=FSMAdmin.create_region)


register_handlers_admin(dp)
