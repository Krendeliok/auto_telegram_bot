from telegram import dp
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from ..contexts import FSMAdvertisement

from cloudinary import uploader

from ..queries.exists import (
    exists_producer,
    exists_model_from_producer,
    exists_engine_type,
    exists_gearbox,
    exists_city,
    exists_drive_unit,
)
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
    drive_unit_keyboard,
)
from datetime import date
from ..texts import RULES

from config import MAX_IMAGES

from ..commands import general, special
from .general import start_command

from ..utils import (
    make_advertisement,
    check_vin,
)


async def add_cloudinary_source_to_images(message, images):
    for image in images:
        file = await message.bot.get_file(image["source"])
        file_url = message.bot.get_file_url(file.file_path)
        upload_response = uploader.upload(file_url, folder="autoyarmarok")
        image["cloudinary_source"] = upload_response["url"]
    return images


async def start_advertisement(message: types.Message, state: FSMContext):
    can_create, kind = can_create_and_kind_adv(telegram_id=message.from_user.id)
    if can_create:
        await FSMAdvertisement.producer.set()
        await state.update_data({"kind": kind})
        await message.answer(RULES)
        await message.answer("Оберіть марку машини", reply_markup=producers_keyboard())
    else:
        await message.answer("❌Ліміт оголошень вичерпано.\nВи можети придбати більший.",
                             reply_markup=commands_keyboard(message.chat.id))


async def cancel_handler(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return
    await state.finish()
    await message.reply("Скасовано!", reply_markup=commands_keyboard(message.from_user.id))


def back_handler(previous_func, key=None, alt_func=None, alt_key=None):
    def wrapper(func):
        async def inner(message, state, *args, **kwargs):
            if message.text == special["back"]:
                if alt_func and any([is_admin(message.from_user.id), is_owner(message.from_user.id)]):
                    async with state.proxy() as data:
                        message.text = data[alt_key]
                    await alt_func(message, state=state)
                    return
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
        await message.reply("❌Це не схоже на марку. Спробуйте обрати з доступних.", reply_markup=producers_keyboard())


@back_handler(previous_func=start_advertisement)
async def set_model(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        exists, obj = exists_model_from_producer(message.text, data["producer"])
        if exists:
            data["model_id"] = obj.id
            data["model"] = message.text
            await state.set_state(FSMAdvertisement.vin)
            await message.answer("Напишіть VIN номер авто.", reply_markup=back_complete_keyboard(deny=True, skip=True))
        else:
            await message.reply(
                "❌Не знаю таку модель від вказаного виробника. Спробуйте обрати з доступних.",
                reply_markup=models_keyboard(producer_name=data["producer"])
            )


@back_handler(previous_func=set_producer, key="producer")
async def set_vin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == special["skip"] or message.text is None:
            data["vin"] = None
        else:
            if not check_vin(message.text):
                await message.answer("❌VIN номер має бути 17 символів. Спробуйте ще раз.",
                                     reply_markup=back_complete_keyboard(deny=True, skip=True))
                return
            else:
                data["vin"] = message.text
        await state.set_state(FSMAdvertisement.price)
        await message.answer("Напишіть ціну у долларах.", reply_markup=back_complete_keyboard(deny=True))


@back_handler(previous_func=set_model, key="model")
async def set_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        if price > 1_000_000:
            await message.answer("❌Ціну більшу за 1 000 000 встановити не вийде.",
                                 reply_markup=back_complete_keyboard(deny=True))
            return
        if price <= 0:
            await message.answer("❌Ціна повинна бути більше 0.", reply_markup=back_complete_keyboard(deny=True))
            return
        async with state.proxy() as data:
            data["price"] = price
        await state.set_state(FSMAdvertisement.year)
        await message.answer("Якого року ваша машина?", reply_markup=back_complete_keyboard(deny=True))
    except ValueError:
        await message.reply("❌Ціна має бути цілим числом та написана у долларах.",
                            reply_markup=back_complete_keyboard(deny=True))


@back_handler(previous_func=set_vin, key="vin")
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
            await message.reply(f"❌Рік може бути у діапазоні від 1970 року до {current_year}.")
    except ValueError:
        await message.reply("❌Рік має бути цілим числом. Спробуйте ще раз.",
                            reply_markup=back_complete_keyboard(deny=True))


@back_handler(previous_func=set_price, key="price")
async def set_engine_type(message: types.Message, state: FSMContext):
    exists, obj = exists_engine_type(message.text)
    if exists:
        async with state.proxy() as data:
            data["engine_type_id"] = obj.id
            data["engine_type"] = message.text
        await state.set_state(FSMAdvertisement.engine_volume)
        if message.text == "Електро":
            await message.answer("Напишіть потужність двигуна(кВт).", reply_markup=back_complete_keyboard(deny=True))
        else:
            await message.answer("Напишіть об'єм двигуна(л). Наприклад: 2.2 або 3",
                                 reply_markup=back_complete_keyboard(deny=True))
    else:
        await message.reply("❌Я не пам'ятаю щоб таке паливо використовував автомобіль. Спробуйте обрати з доступних.",
                            reply_markup=engine_keyboard())


@back_handler(previous_func=set_year, key="year")
async def set_engine_volume(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        if data["engine_type"] == "Електро":
            power = int(message.text)
            if power <= 0.0 or power > 1500:
                await message.answer("❌Потужність повинна бути більше 0 та не більше 1500 кВт.",
                                     reply_markup=back_complete_keyboard(deny=True))
                return
            async with state.proxy() as data:
                data["engine_volume"] = power
        else:
            volume = round(float(message.text), 1)
            if volume <= 0.0 or volume > 20.0:
                await message.answer("❌Об'єм повинен бути більше 0 та не більше 20.",
                                     reply_markup=back_complete_keyboard(deny=True))
                return
            async with state.proxy() as data:
                data["engine_volume"] = volume
        await state.set_state(FSMAdvertisement.range)
        await message.answer("Напишіть пробіг авто (тис. км.) від 1 до 999",
                             reply_markup=back_complete_keyboard(deny=True))
    except ValueError:
        await message.reply("❌Сталася помилка. Спробуйте вказати об'єм ще раз як у прикладі.",
                            reply_markup=back_complete_keyboard(deny=True))


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
        await message.reply("❌Пробіг треба вказувати цілим числом від 1 до 999. Спробуйте ще раз.")


@back_handler(previous_func=set_engine_volume, key="engine_volume")
async def set_gearbox(message: types.Message, state: FSMContext):
    exists, obj = exists_gearbox(message.text)
    if exists:
        await state.set_state(FSMAdvertisement.drive_unit)
        async with state.proxy() as data:
            data["gearbox_type_id"] = obj.id
            data["gearbox_type"] = message.text

        await message.answer("Вкажіть привід.", reply_markup=drive_unit_keyboard())
    else:
        await message.reply("❌Не знаю такого типу коробки. Спробуйте обрати з доступних.", reply_markup=gearbox_keyboard())


@back_handler(previous_func=set_range, key="range")
async def set_drive_unit(message: types.Message, state: FSMContext):
    exists, obj = exists_drive_unit(message.text)
    if exists:
        await state.set_state(FSMAdvertisement.city)
        async with state.proxy() as data:
            data["drive_unit_id"] = obj.id
            data["drive_unit"] = message.text

            if is_spam(data, message.from_user.id):
                await message.answer("⭕️Таке оголошення у вас вже є, ви не зможете повторно його відправити",
                                     reply_markup=back_complete_keyboard(deny=True))
                return

        await message.answer("Оберіть область знаходження.", reply_markup=country_keyboard())
    else:
        await message.reply("❌Не знаю такого приводу. Спробуйте обрати з доступних.", reply_markup=drive_unit_keyboard())


@back_handler(previous_func=set_gearbox, key="gearbox_type")
async def set_city(message: types.Message, state: FSMContext):
    exists, obj = exists_city(message.text)
    if exists:
        async with state.proxy() as data:
            data["based_country_id"] = obj.id
            data["based_country"] = message.text
        await state.set_state(FSMAdvertisement.description)
        await message.answer("Зробіть опис для машини.", reply_markup=back_complete_keyboard(deny=True))
    else:
        await message.reply("❌Вперше чую про таку область. Спробуйте обрати найближчу до вас з доступних.",
                            reply_markup=country_keyboard())


@back_handler(previous_func=set_drive_unit, key="drive_unit")
async def set_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text

    if is_admin(message.from_user.id) or is_owner(message.from_user.id):
        await state.set_state(FSMAdvertisement.phone_numbers)
        await message.answer("Які номера телефону зазначити в оголошенні?", reply_markup=phone_numbers_keyboard())
    else:
        await state.set_state(FSMAdvertisement.images)
        await message.answer(f"Відправте до {MAX_IMAGES} фото.\nПісля завершення натисніть {special['complete']}",
                             reply_markup=back_complete_keyboard(deny=True, complete=True))


@back_handler(previous_func=set_city, key="based_country")
async def set_phone_numbers(message: types.Message, state: FSMContext):
    if message.text == special["private_phone"]:
        phone = get_user_phone(message.from_user.id)
    elif message.text == special["comercial_phone"]:
        phone = "+380506200777 / +380976200777"

    async with state.proxy() as data:
        data["phone"] = phone

    await state.set_state(FSMAdvertisement.images)
    await message.answer(f"Відправте до {MAX_IMAGES} фото.\nПісля завершення натисніть {special['complete']}",
                         reply_markup=back_complete_keyboard(deny=True, complete=True))


@back_handler(previous_func=set_city, key="based_country", alt_func=set_description, alt_key="description")
async def set_images(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data["image_counter"] = 1
            data["images"] = [{"source": message.photo[-1].file_id}]
        await state.set_state(FSMAdvertisement.more_images)


@back_handler(previous_func=set_city, key="based_country", alt_func=set_description, alt_key="description")
async def more_images(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data["image_counter"] < int(MAX_IMAGES):
            data["image_counter"] += 1
            data["images"].append({"source": message.photo[-1].file_id})
        else:
            await message.answer(f"🟠Фотографій вже забагато, я залишу тільки перші {MAX_IMAGES}",
                                 reply_markup=back_complete_keyboard(deny=True, complete=True))


@back_handler(previous_func=set_city, key="based_country", alt_func=set_description, alt_key="description")
async def submition_advertisement(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["images"] = await add_cloudinary_source_to_images(message, data["images"])
        adv_id = await create_advertisement(data)
    await message.answer("✅Пост відправлено адміну. Через деякий час вам надішлеться відповідь.",
                         reply_markup=commands_keyboard(message.from_user.id))
    adv = await get_advertisement_by_id(adv_id)
    await submit_to_admin_for_approval(message, adv)

    await state.finish()


async def submit_to_admin_for_approval(message: types.Message, adv):
    random_admin = get_random_admin()
    if random_admin:
        media_group = make_advertisement(adv)
        await message.bot.send_media_group(
            random_admin.telegram_id,
            media=media_group,
        )
        await message.bot.send_message(
            random_admin.telegram_id,
            "Що зробити з оголошенням?",
            reply_markup=adverisement_keyboard(f'approve:{adv["id"]}', f'reject:{adv["id"]}')
        )
        pin_admin(adv["id"], random_admin.id)


def register_handlers_advertisement(dp: Dispatcher):
    dp.register_message_handler(start_advertisement, Text(equals=general["new_adv"], ignore_case=True), state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=special["end"])
    dp.register_message_handler(cancel_handler, Text(equals=special["end"], ignore_case=True), state="*")
    dp.register_message_handler(set_producer, state=FSMAdvertisement.producer)
    dp.register_message_handler(set_model, state=FSMAdvertisement.model)
    dp.register_message_handler(set_vin, state=FSMAdvertisement.vin)
    dp.register_message_handler(set_price, state=FSMAdvertisement.price)
    dp.register_message_handler(set_year, state=FSMAdvertisement.year)
    dp.register_message_handler(set_engine_type, state=FSMAdvertisement.engine_type)
    dp.register_message_handler(set_engine_volume, state=FSMAdvertisement.engine_volume)
    dp.register_message_handler(set_range, state=FSMAdvertisement.range)
    dp.register_message_handler(set_gearbox, state=FSMAdvertisement.gearbox)
    dp.register_message_handler(set_drive_unit, state=FSMAdvertisement.drive_unit)
    dp.register_message_handler(set_city, state=FSMAdvertisement.city)
    dp.register_message_handler(set_description, state=FSMAdvertisement.description)
    dp.register_message_handler(set_phone_numbers, state=FSMAdvertisement.phone_numbers)
    dp.register_message_handler(set_images, content_types=["photo", "text"], state=FSMAdvertisement.images)
    dp.register_message_handler(submition_advertisement, Text(equals=special["complete"], ignore_case=True),
                                state=FSMAdvertisement.more_images)
    dp.register_message_handler(more_images, content_types=["photo"], state=FSMAdvertisement.more_images)


register_handlers_advertisement(dp)
