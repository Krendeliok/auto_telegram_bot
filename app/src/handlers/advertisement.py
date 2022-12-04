from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InputMediaPhoto, MediaGroup

from ..contexts import FSMAdvertisement, FSMMenu

from ..queries import (
    exists_producer,
    exists_model_from_producer,
    exists_engine_type,
    exists_gearbox,
    exists_city,
    create_advertisement,
    get_random_admin,
    pin_admin,
    get_advertisement,
)

from ..keyboards import (
    producers_keyboard, 
    models_keyboard,
    engine_keyboard,
    gearbox_keyboard,
    country_keyboard,
    adverisement_keyboard,
    hide_keyboard,
    commands_keyboard,
    back_complete_keyboard
)
from datetime import date
from ..texts import RULES

from config import MAX_IMAGES

from ..commands import general, special
from .general import start_command


async def start_advertisement(message: types.Message, state: FSMContext):
    await FSMAdvertisement.producer.set()
    await message.answer(RULES)
    await message.answer("Оберіть марку машини", reply_markup=producers_keyboard())

async def cancel_handler(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return
    await state.finish()
    await message.reply("Скасовано!", reply_markup=commands_keyboard(message.from_user.id))

def back_handler(previous_func, key=None):
    def wrapper(func):
        async def inner(message, state, *args, **kwargs):
            if message.text == str(special["back"]):
                if key is not None:
                    async with state.proxy() as data:
                        message.text = data[key]
                await previous_func(message=message, state=state)
                return
            await func(message=message, state=state)
        return inner
    return wrapper

@back_handler(previous_func=start_command)
async def set_producer(message: types.Message, state: FSMContext):
    exists, _ = exists_producer(message.text)
    if exists:
        async with state.proxy() as data:
            data["producer"] = message.text
            data["user_id"] = message.from_user.id
        await state.set_state(FSMAdvertisement.model)
        await message.answer("Оберіть модель машини.", reply_markup=models_keyboard(producer_name=message.text))
    else:
        await message.reply("Це не схоже на марку. Спробуйте обрати з доступних.", reply_markup=producers_keyboard())

@back_handler(previous_func=start_advertisement)
async def set_model(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        exists, obj = exists_model_from_producer(message.text, data["producer"])
        if exists:
            data["model_id"] = obj.id
            data["model"] = message.text
            await state.set_state(FSMAdvertisement.price)
            await message.answer("Напишіть ціну у долларах.", reply_markup=back_complete_keyboard(deny=True))
        else:
            await message.reply(
                "Не знаю таку модель від вказаного виробника. Спробуйте обрати з доступних.", 
                reply_markup=models_keyboard(producer_name=data["producer"])
                )

@back_handler(previous_func=set_producer, key="producer")
async def set_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        async with state.proxy() as data:
            data["price"] = price
        await state.set_state(FSMAdvertisement.year)
        await message.answer("Якого року ваша машина?", reply_markup=back_complete_keyboard(deny=True))
    except ValueError:
        await message.reply("Ціна має бути цілим числом та написана у долларах.")

@back_handler(previous_func=set_model, key="model")
async def set_year(message: types.Message, state: FSMContext):
    try:
        year = int(message.text)
        current_year = date.today().year
        if 1970 <= year <= current_year:
            async with state.proxy() as data:
                data["year"] = year
            await state.set_state(FSMAdvertisement.engine_type)
            await message.answer("Оберіть тип палива.", reply_markup=engine_keyboard())
        else:
            await message.reply(f"Рік може бути у діапазоні від 1970 року до {current_year}.")
    except ValueError:
        await message.reply("Рік має бути цілим числом. Спробуйте ще раз.")


@back_handler(previous_func=set_price, key="price")
async def set_engine_type(message: types.Message, state: FSMContext):
    exists, obj = exists_engine_type(message.text)
    if exists:
        async with state.proxy() as data:
            data["engine_type_id"] = obj.id
            data["engine_type"] = message.text
        await state.set_state(FSMAdvertisement.engine_volume)
        await message.answer("Напишіть об'єм двигуна. Наприклад: 2.2 або 3", reply_markup=back_complete_keyboard(deny=True))
    else:
        await message.reply("Я не пам'ятаю щоб таке паливо використовував автомобіль. Спробуйте обрати з доступних.", reply_markup=engine_keyboard())


@back_handler(previous_func=set_year, key="year")
async def set_engine_volume(message: types.Message, state: FSMContext):
    try:
        volume = float(message.text)
        async with state.proxy() as data:
            data["engine_volume"] = volume
        await state.set_state(FSMAdvertisement.range)
        await message.answer("Напишіть пробіг авто (тис. км.) від 1 до 999", reply_markup=back_complete_keyboard(deny=True))
    except ValueError:
        await message.reply("Сталася помилка. Спробуйте вказати об'єм ще раз як у прикладі.")


@back_handler(previous_func=set_engine_type, key="engine_type")
async def set_range(message: types.Message, state: FSMContext):
    try:
        auto_range = int(message.text)
        if 0 < auto_range < 1000:
            async with state.proxy() as data:
                data["range"] = auto_range
            await state.set_state(FSMAdvertisement.gearbox)
            await message.answer("Оберіть тип коробки", reply_markup=gearbox_keyboard())
        else:
            raise ValueError()
    except ValueError:
        await message.reply("Пробіг треба вказувати цілим числом від 1 до 999. Спробуйте ще раз.")


@back_handler(previous_func=set_engine_volume, key="engine_volume")
async def set_gearbox(message: types.Message, state: FSMContext):
    exists, obj = exists_gearbox(message.text)
    if exists:
        async with state.proxy() as data:
            data["gearbox_type_id"] = obj.id
            data["gearbox_type"] = message.text
        await state.set_state(FSMAdvertisement.city)
        await message.answer("Оберіть область знаходження.", reply_markup=country_keyboard())
    else:
        await message.reply("Не знаю такого типу коробки. Спробуйте обрати з доступних.", reply_markup=gearbox_keyboard())


@back_handler(previous_func=set_range, key="range")
async def set_city(message: types.Message, state: FSMContext):
    exists, obj = exists_city(message.text)
    if exists:
        async with state.proxy() as data:
            data["based_country_id"] = obj.id
            data["based_country"] = message.text
        await state.set_state(FSMAdvertisement.description)
        await message.answer("Зробіть опис для машини.", reply_markup=back_complete_keyboard(deny=True))
    else:
        await message.reply("Вперше чую про таку область. Спробуйте обрати найближчу до вас з доступних.", reply_markup=country_keyboard())


@back_handler(previous_func=set_gearbox, key="gearbox_type")
async def set_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await state.set_state(FSMAdvertisement.images)
    await message.answer(f"Відправте до {MAX_IMAGES} фото.\nПісля завершення натисніть {special['complete']}", reply_markup=back_complete_keyboard(deny=True, complete=True))


@back_handler(previous_func=set_city, key="based_country")
async def set_images(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data["image_counter"] = 1
            data["images"] = [message.photo[0].file_id]
        await state.set_state(FSMAdvertisement.more_images)


@back_handler(previous_func=set_city, key="based_country")
async def more_images(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data["image_counter"] < int(MAX_IMAGES):
            data["image_counter"] += 1
            data["images"].append(message.photo[0].file_id)
        else:
            await message.answer(f"Фотографій вже забагато, я залишу тільки перші {MAX_IMAGES}", reply_markup=back_complete_keyboard(deny=True, complete=True))


@back_handler(previous_func=set_city, key="based_country")
async def submition_advertisement(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        adv_id = create_advertisement(data)
    await message.answer("Пост відправлено адміну. Через деякий час вам надішлеться відповідь.", reply_markup=commands_keyboard(message.from_user.id))
    adv = get_advertisement(adv_id)
    await submit_to_admin_for_approval(message, adv)

    await FSMMenu.start.set()

async def submit_to_admin_for_approval(message: types.Message, adv):
    random_admin = get_random_admin()
    images = adv.images
    media_group = MediaGroup()
    media_group.attach(InputMediaPhoto(images[0].source, caption=adv.get_sending_text))
    for image in images[1:]:
        media_group.attach(InputMediaPhoto(image.source))
    await message.bot.send_media_group(
        random_admin.telegram_id,
        media=media_group,
    )
    await message.bot.send_message(
        random_admin.telegram_id,
        "Що зробити з оголошенням?",
        reply_markup=adverisement_keyboard(f"approve:{adv.id}", f"reject:{adv.id}")
    )
    pin_admin(adv.id, random_admin.id)


def register_handlers_advertisement(dp: Dispatcher):
    dp.register_message_handler(start_advertisement, Text(equals=str(general["new_adv"]), ignore_case=True), state=FSMMenu.start)
    dp.register_message_handler(cancel_handler, state="*", commands=str(special["end"]))
    dp.register_message_handler(cancel_handler, Text(equals=str(special["end"]), ignore_case=True), state="*")
    dp.register_message_handler(set_producer, state=FSMAdvertisement.producer)
    dp.register_message_handler(set_model, state=FSMAdvertisement.model)
    dp.register_message_handler(set_price, state=FSMAdvertisement.price)
    dp.register_message_handler(set_year, state=FSMAdvertisement.year)
    dp.register_message_handler(set_engine_type, state=FSMAdvertisement.engine_type)
    dp.register_message_handler(set_engine_volume, state=FSMAdvertisement.engine_volume)
    dp.register_message_handler(set_range, state=FSMAdvertisement.range)
    dp.register_message_handler(set_gearbox, state=FSMAdvertisement.gearbox)
    dp.register_message_handler(set_city, state=FSMAdvertisement.city)
    dp.register_message_handler(set_description, state=FSMAdvertisement.description)
    dp.register_message_handler(set_images, content_types=["photo", "text"], state=FSMAdvertisement.images)
    dp.register_message_handler(submition_advertisement, Text(equals=str(special["complete"]), ignore_case=True), state=FSMAdvertisement.more_images)
    dp.register_message_handler(more_images, content_types=["photo"], state=FSMAdvertisement.more_images)