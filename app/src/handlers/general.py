from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import MediaGroup, InputMediaPhoto

from ..keyboards import (
    contact_keyboard, 
    commands_keyboard, 
    filter_commands,
    producers_keyboard,
    country_keyboard,
    engine_keyboard,
    gearbox_keyboard,
    models_keyboard,
    filter_buttons,
)
from ..queries import (
    exists_producer,
    exists_model_from_producer,
    exists_engine_type,
    exists_gearbox,
    exists_city,
    create_client, 
    exists_client,
    get_user_filter,
    add_filter_producer,
    add_filter_model,
    add_filter_gearbox,
    add_filter_engine,
    add_filter_region,
    add_filter_engine_volume,
    add_filter_price,
    add_filter_range,
    add_filter_year,
    remove_producer_from_filter,
    get_advertisements_by_filter
)

from ..contexts import FSMMenu, FSMFilter
from ..commands import general, filters, special


async def start_command(message: types.Message, state: FSMContext, **kwargs):
    exists, model = exists_client(message.from_user.id)
    if exists:
        await message.answer("Вітаю!\nЩо хочете зробити?", reply_markup=commands_keyboard(message.from_user.id))
        await state.finish()
    else:
        await message.answer("Для початку треба вас ідентифікувати.\nВідправте будь ласка ваш контакт.", reply_markup=contact_keyboard())
        await FSMMenu.contact.set()


async def get_contact(message: types.Message, state: FSMContext):
    create_client(message)
    await message.answer("Дякую, ваші дані занесені у базу даних.\nМожете продовжувати роботу.", reply_markup=commands_keyboard())
    await state.finish()


async def start_filter(message: types.Message, state: FSMContext, *args, **kwargs):
    await message.answer("Оберіть як треба фільтрувати.", reply_markup=filter_commands())
    await FSMFilter.start.set()

def back_handler(previous_func, text=None):
    def wrapper(func):
        async def inner(message, state, user_filter=None, *args, **kwargs):
            if message.text == str(special["back"]):
                if text is not None:
                    message.text = text
                await previous_func(message=message, state=state, user_filter=user_filter)
                return
            await func(message=message, state=state, user_filter=user_filter, previous_func=previous_func, text=text, *args, **kwargs)
        return inner
    return wrapper

@back_handler(previous_func=start_command)
async def filter_commands_handler(message: types.Message, state: FSMContext, *args, **kwargs):
    if message.text == str(special["find"]):
        await search_filter(message, state)
    elif message.text == str(filters["producer"]):
        await FSMFilter.producer.set()
        await message.answer("Оберіть яку марку хочете відстежувати.", reply_markup=producers_keyboard(filter_buttons=True, telegram_id=message.from_user.id))
    elif message.text == str(filters["gearbox"]):
        await FSMFilter.gearbox.set()
        await message.answer("Оберіть модель яку треба відстежувати.", reply_markup=gearbox_keyboard(filter_buttons=True, telegram_id=message.from_user.id))
    elif message.text == str(filters["region"]):
        await FSMFilter.region.set()
        await message.answer("Оберіть область для фільтру", reply_markup=country_keyboard(filter_buttons=True, telegram_id=message.from_user.id))
    elif message.text == str(filters["engine_type"]):
        await FSMFilter.engine_type.set()
        await message.answer("Оберіть тип палива для фільтру", reply_markup=engine_keyboard(filter_buttons=True, telegram_id=message.from_user.id))
    elif message.text == str(filters["price"]):
        await FSMFilter.price.set()
        await message.answer("Вкажіть ціну для фільтру. Формат(мін-макс, -макс, мін-)", reply_markup=filter_buttons())
    elif message.text == str(filters["year"]):
        await FSMFilter.year.set()
        await message.answer("Вкажіть рік для фільтру. Формат(мін-макс, -макс, мін-)", reply_markup=filter_buttons())
    elif message.text == str(filters["engine_volume"]):
        await FSMFilter.engine_volume.set()
        await message.answer("Вкажіть обїєм двигуна для фільтру. Формат(мін-макс, -макс, мін-)", reply_markup=filter_buttons())
    elif message.text == str(filters["range"]):
        await FSMFilter.range.set()
        await message.answer("Вкажіть пробіг для фільтру. Формат(мін-макс, -макс, мін-)", reply_markup=filter_buttons())


def filter_handler(add_filter=None, plural_model=""):
    def wrapper(func):
        async def inner(message: types.Message, state: FSMContext, user_filter, previous_func, text=None, *args, **kwargs):
            message.text = message.text.split("✅")[0].split("🟠")[0]
            if message.text == str(special["all"]) and add_filter:
                await message.answer(f"Усі {plural_model} додані успішно.")
                if text is not None:
                    async with state.proxy() as data:
                        add_filter(data["producer_filter_id"], set_all=True)
                    message.text = text
                else:
                    add_filter(user_filter, set_all=True)

                await previous_func(message, state, user_filter)
                return
            elif message.text == str(special["remove_producer"]):
                async with state.proxy() as data:
                    remove_producer_from_filter(user_filter.id, data["producer"])
                message.text = text
                await previous_func(message, state, user_filter)
                return
            await func(message, state, user_filter)
        return inner
    return wrapper

def add_user_filter(func):
    async def wrapper(message: types.Message, state: FSMContext):
        user_filter = get_user_filter(message.from_user.id)
        await func(message, state, user_filter)
    return wrapper

def get_min_max(text, res_type):
    return [res_type(i or 0) for i in text.split("-")]

async def add_number_value_to_filter(message: types.Message, state: FSMContext, filter_func, res_type):
    if "-" in message.text:
        try:
            user_filter = get_user_filter(message.from_user.id)
            mn, mx = get_min_max(message.text, res_type)
            filter_func(user_filter, mn, mx)
            await start_filter(message, state)
        except ValueError:
            await message.answer("wrong format")
    
async def send_adv(message: types.Message, adv):
    images = adv.images
    media_group = MediaGroup()
    media_group.attach(InputMediaPhoto(images[0].source, caption=adv.get_sending_text))
    for image in images[1:]:
        media_group.attach(InputMediaPhoto(image.source))
    await message.bot.send_media_group(
            message.from_user.id,
            media=media_group
    )

@add_user_filter
async def search_filter(message: types.Message, state: FSMContext, user_filter):
    advs = get_advertisements_by_filter(user_filter)
    await message.answer(f"По вашому фільтру було знайдено {len(advs)} оголошень.")
    for adv in advs:
        await send_adv(message, adv)

@add_user_filter
@back_handler(previous_func=start_filter)
@filter_handler(add_filter=add_filter_producer, plural_model="марки")
async def filter_producer(message: types.Message, state: FSMContext, user_filter):
    exists, obj = exists_producer(message.text)
    if exists:
        async with state.proxy() as data:
            data["producer"] = message.text
            producer_filter = add_filter_producer(user_filter, producer_id=obj.id)
            data["producer_filter_id"] = producer_filter.id
        await state.set_state(FSMFilter.model)
        await message.answer("Оберіть модель машини.", reply_markup=models_keyboard(producer_name=message.text, filter_buttons=True, telegram_id=message.from_user.id))
    else:
        await message.reply("Це не схоже на марку. Спробуйте обрати з доступних.", reply_markup=producers_keyboard(filter_buttons=True, telegram_id=message.from_user.id))

@add_user_filter
@back_handler(previous_func=filter_commands_handler, text=str(filters["producer"]))
@filter_handler(add_filter=add_filter_model, plural_model="моделі")
async def filter_model(message: types.Message, state: FSMContext, *args):
    async with state.proxy() as data:
        exists, obj = exists_model_from_producer(message.text, data["producer"])
        if exists:
            created, _ = add_filter_model(data["producer_filter_id"], model_id=obj.id)
            await message.answer(
                f"Модель {message.text} марки {data['producer']} {'додана' if created else 'видалена'} успішно.",
                reply_markup=models_keyboard(producer_name=data["producer"], filter_buttons=True, telegram_id=message.from_user.id)
                )
        else:
            await message.reply(
                "Не знаю таку модель від вказаного виробника. Спробуйте обрати з доступних.", 
                reply_markup=models_keyboard(producer_name=data["producer"], filter_buttons=True, telegram_id=message.from_user.id)
            )

@add_user_filter
@back_handler(previous_func=start_filter)
@filter_handler(add_filter=add_filter_engine, plural_model="палива")
async def filter_engine_types(message: types.Message, state: FSMContext, user_filter):
    exists, obj = exists_engine_type(message.text)
    if exists:
        created, _ = add_filter_engine(user_filter, engine_id=obj.id)
        await message.answer(f"Тип палива {message.text} {'додана' if created else 'видалена'} успішно.", reply_markup=engine_keyboard(filter_buttons=True, telegram_id=message.from_user.id))
    else:
        await message.reply("Я не пам'ятаю щоб таке паливо використовував автомобіль. Спробуй обрати з доступних.", reply_markup=engine_keyboard(filter_buttons=True, telegram_id=message.from_user.id))

@add_user_filter
@back_handler(previous_func=start_filter)
@filter_handler(add_filter=add_filter_gearbox, plural_model="коробки")
async def filter_gearbox(message: types.Message, state: FSMContext, user_filter):
    exists, obj = exists_gearbox(message.text)
    if exists:
        created, _ = add_filter_gearbox(user_filter, gearbox_id=obj.id)
        await message.answer(f"Коробка {message.text} {'додана' if created else 'видалена'} успішно.", reply_markup=gearbox_keyboard(filter_buttons=True, telegram_id=message.from_user.id))
    else:
        await message.reply("Не знаю такого типу коробки. Спробуйте обрати з доступних.", reply_markup=gearbox_keyboard(filter_buttons=True, telegram_id=message.from_user.id))

@add_user_filter
@back_handler(previous_func=start_filter)
@filter_handler(add_filter=add_filter_region, plural_model="області")
async def filter_region(message: types.Message, state: FSMContext, user_filter):
    exists, obj = exists_city(message.text)
    if exists:
        created, _ = add_filter_region(user_filter, region_id=obj.id)
        await message.answer(f"Область {message.text} {'додана' if created else 'видалена'} успішно.", reply_markup=country_keyboard(filter_buttons=True, telegram_id=message.from_user.id))
    else:
        await message.reply("Вперше чую про таку область. Спробуйте обрати найближчу до вас з доступних.", reply_markup=country_keyboard(filter_buttons=True, telegram_id=message.from_user.id))

@add_user_filter
@back_handler(previous_func=start_filter)
@filter_handler()
async def filter_price(message: types.Message, state: FSMContext, *args):
    await add_number_value_to_filter(message, state, add_filter_price, res_type=int)
        
@add_user_filter
@back_handler(previous_func=start_filter)
@filter_handler()
async def filter_volume(message: types.Message, state: FSMContext, *args):
    await add_number_value_to_filter(message, state, add_filter_engine_volume, res_type=float)

@add_user_filter
@back_handler(previous_func=start_filter)
@filter_handler()
async def filter_year(message: types.Message, state: FSMContext, *args):
    await add_number_value_to_filter(message, state, add_filter_year, res_type=int)

@add_user_filter
@back_handler(previous_func=start_filter)
@filter_handler()
async def filter_range(message: types.Message, state: FSMContext, *args):
    await add_number_value_to_filter(message, state, add_filter_range, res_type=int)


def register_hendlers_general(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'], state="*")
    dp.register_message_handler(get_contact, content_types=types.ContentType.CONTACT, state=FSMMenu.contact)
    dp.register_message_handler(start_filter, Text(equals=str(general["filter"]), ignore_case=True), state=None)
    dp.register_message_handler(filter_commands_handler, state=FSMFilter.start)
    dp.register_message_handler(filter_producer, state=FSMFilter.producer)
    dp.register_message_handler(filter_model, state=FSMFilter.model)
    dp.register_message_handler(filter_engine_types, state=FSMFilter.engine_type)
    dp.register_message_handler(filter_gearbox, state=FSMFilter.gearbox)
    dp.register_message_handler(filter_region, state=FSMFilter.region)
    dp.register_message_handler(filter_price, state=FSMFilter.price)
    dp.register_message_handler(filter_volume, state=FSMFilter.engine_volume)
    dp.register_message_handler(filter_year, state=FSMFilter.year)
    dp.register_message_handler(filter_range, state=FSMFilter.range)