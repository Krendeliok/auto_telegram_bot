from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import MediaGroup, InputMediaPhoto
from config import CHANNEL_NAME

from ..contexts import (FSMCreateCity, FSMCreateEngineType, FSMCreateGearbox,
                        FSMCreateModel, FSMCreateProducer, FSMSolution)
from ..keyboards import producers_keyboard, commands_keyboard, hide_keyboard
from ..queries import (create_city, create_engine_type, create_gearbox,
                       create_model, create_producer, exists_producer,
                       get_advertisement, is_admin, update_adv_status)

from ..commands import admin, special


async def submit_advertisement(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.bot.answer_callback_query(callback_query.id)
    status, adv_id = callback_query["data"].split(":")
    update_adv_status(int(adv_id), status == "approve")
    adv = get_advertisement(int(adv_id))
    await callback_query.message.delete()
    if status == "approve":
        await send_to_channel(callback_query.message, adv)
        await callback_query.message.answer("Погоджено!")
        await callback_query.bot.send_message(
            adv.client.telegram_id, 
            "Ваша об'ява погоджена і буде виставлятися раз на місяць.", 
            reply_markup=commands_keyboard(adv.client.telegram_id)
        )
    elif status == "reject":
        await callback_query.message.answer("Відхилено!")
        await FSMSolution.message.set()
        await state.update_data(user_id=adv.client.telegram_id)
        await callback_query.bot.send_message(callback_query.from_user.id, "Напишіть причину відмови.", reply_markup=hide_keyboard())

async def send_reject_message(message: types.Message, state: FSMContext):
    reject_message = message.text
    async with state.proxy() as data:
        await message.bot.send_message(
            data["user_id"], 
            f"Вашу об'яву відхилено. Причина: {reject_message}.", 
            reply_markup=commands_keyboard(message.from_user.id)
        )
    await state.finish()

async def send_to_channel(message, adv):
    images = adv.images
    media_group = MediaGroup()
    media_group.attach(InputMediaPhoto(images[0].source, caption=adv.get_sending_text))
    for image in images[1:]:
        media_group.attach(InputMediaPhoto(image.source))
    await message.bot.send_media_group(
            CHANNEL_NAME,
            media=media_group
    )

async def admin_creation_start(message: types.Message):
    if is_admin(message.from_user.id):
        if message.text == admin["admin"].get_command:
            await message.answer("Оберіть команду.", reply_markup=commands_keyboard(message.from_user.id))
        elif message.text == admin["create_producer"].get_command:
            await FSMCreateProducer.producer_name.set()
            await message.answer("Вкажіть ім'я нової марки.")
        elif message.text == admin["create_model"].get_command:
            await FSMCreateModel.model_name.set()
            await message.answer("Вкажіть ім'я нової моделі.")
        elif message.text == admin["create_city"].get_command:
            await FSMCreateCity.city_name.set()
            await message.answer("Вкажіть ім'я нової області.")
        elif message.text == admin["create_engine_type"].get_command:
            await FSMCreateEngineType.engine_name.set()
            await message.answer("Вкажіть ім'я нового типу палива.")
        elif message.text == admin["create_gearbox"].get_command:
            await FSMCreateGearbox.gearbox_name.set()
            await message.answer("Вкажіть ім'я нової коробки.")

async def cancel_handler(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return
    await state.finish()
    await message.reply("Скасовано!", reply_markup=commands_keyboard(message.from_user.id))

async def admin_create_producer(message: types.Message, state: FSMContext):
    await state.finish()
    create_producer(message.text)
    await message.answer("Марка створена.", reply_markup=commands_keyboard(message.from_user.id))

async def admin_create_engine_type(message: types.Message, state: FSMContext):
    await state.finish()
    create_engine_type(message.text)
    await message.answer("Тип палива створений.", reply_markup=commands_keyboard(message.from_user.id))

async def admin_create_city(message: types.Message, state: FSMContext):
    await state.finish()
    create_city(message.text)
    await message.answer("Область створена.", reply_markup=commands_keyboard(message.from_user.id))

async def admin_create_gearbox(message: types.Message, state: FSMContext):
    await state.finish()
    create_gearbox(message.text)
    await message.answer("Коробка створена.", reply_markup=commands_keyboard(message.from_user.id))

async def admin_create_model_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMCreateModel.next()
    await message.answer("Оберіть марку машини.", reply_markup=producers_keyboard())

async def admin_create_model(message: types.Message, state: FSMContext):
    exists, obj = exists_producer(message.text)
    if exists:
        async with state.proxy() as data:
            create_model(data["name"], obj.id)
        await state.finish()
        await message.answer("Модель створена.", reply_markup=commands_keyboard(message.from_user.id))
    else:
        await message.reply("Це не схоже на марку. Спробуйте обрати з доступних.", reply_markup=producers_keyboard())
    

def register_handlers_admin(dp: Dispatcher):
    dp.register_callback_query_handler(
        submit_advertisement, 
        lambda c: c.data.startswith("approve") or c.data.startswith("reject"), 
        state=None
    )
    dp.register_message_handler(send_reject_message, state=FSMSolution.message)
    dp.register_message_handler(admin_creation_start, commands=[str(i) for i in admin.values()])
    dp.register_message_handler(cancel_handler, state="*", commands=[str(special["end"])])
    dp.register_message_handler(cancel_handler, Text(equals=str(special["end"]), ignore_case=True), state="*")
    dp.register_message_handler(admin_create_producer, state=FSMCreateProducer.producer_name)
    dp.register_message_handler(admin_create_model_name, state=FSMCreateModel.model_name)
    dp.register_message_handler(admin_create_model, state=FSMCreateModel.producer)
    dp.register_message_handler(admin_create_engine_type, state=FSMCreateEngineType.engine_name)
    dp.register_message_handler(admin_create_gearbox, state=FSMCreateGearbox.gearbox_name)
    dp.register_message_handler(admin_create_city, state=FSMCreateCity.city_name)
