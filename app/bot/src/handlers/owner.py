from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from ..queries.client import (
    is_owner,
    is_admin,
    set_admin,
    remove_admin,
    get_client_by_username,
)

from ..queries.advertisement import (
    get_advertisement_by_id
)

from ..queries.feedback import (
    get_not_verified_feedbacks,
    set_verified_feedback
)

from ..utils import make_advertisement

from ..contexts import (
    FSMOwner
)
from ..keyboards import (
    clients_keyboard,
    admins_keyboard,
    commands_keyboard,
    show_advertisement,
)

from .general import start_command

from ..commands import owner, special


async def owner_start_commands(message: types.Message):
    if is_owner(message.from_user.id):
        if message.text == owner["create_admin"]:
            await FSMOwner.create_admin.set()
            await message.answer("Оберіть юзера якого треба зробити адміном.", reply_markup=clients_keyboard(ignore_admins=True))
        elif message.text == owner["remove_admin"]:
            await FSMOwner.delete_admin.set()
            await message.answer("Оберіть юзера якого треба позбавити прав адміна", reply_markup=admins_keyboard())
        elif message.text == owner["show_admins"]:
            await FSMOwner.show_admins.set()
            await message.answer("Ось усі адміни", reply_markup=admins_keyboard())
        elif message.text == owner["show_feedbacks"]:
            feedbacks = await get_not_verified_feedbacks()
            if len(feedbacks) == 0:
                await message.answer("Нічого немає")
                return
            for feedback in feedbacks:
                if all((feedback["name"], feedback["phone"])):
                    keyboard = None
                    if feedback.get("advertisement_id"):
                        keyboard = show_advertisement(feedback["advertisement_id"])
                    await message.answer(f"{feedback['name']} {feedback['phone']}", reply_markup=keyboard)
                    await set_verified_feedback(feedback["id"])

async def show_advertisement_handler(callback_query: types.CallbackQuery):
    await callback_query.bot.answer_callback_query(callback_query.id)
    _, adv_id = callback_query["data"].split(":")
    adv = await get_advertisement_by_id(adv_id)
    media_group = make_advertisement(adv)
    await callback_query.bot.send_media_group(
        callback_query.message.chat.id,
        media=media_group
    )

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


@back_handler(previous_func=start_command)
async def create_admin(message: types.Message, state: FSMContext):
    model = get_client_by_username(message.text)
    if model is not None and not is_admin(model.telegram_id):
        set_admin(model.telegram_id)
        await state.finish()
        await message.reply("Адмін успішно створений!", reply_markup=commands_keyboard(message.from_user.id))
    else:
        await message.reply("❌Я не знаю такого користувача або він вже адмін!")


@back_handler(previous_func=start_command)
async def delete_admin(message: types.Message, state: FSMContext):
    model = get_client_by_username(message.text)
    if model is not None and is_admin(model.telegram_id):
        remove_admin(model.telegram_id)
        await state.finish()
        await message.reply("Успішно позбавлено прав адміна", reply_markup=commands_keyboard(message.from_user.id))
    else:
        await message.reply("❌Я не знаю такого користувача або він не адмін!")


@back_handler(previous_func=start_command)
async def show_admins(message: types.Message, state: FSMContext):
    # TODO document why this method is empty
    pass


def register_handlers_owner(dp: Dispatcher):
    dp.register_callback_query_handler(
        show_advertisement_handler,
        lambda c: c.data.startswith("show_adv"),
        state="*"
    )
    dp.register_message_handler(owner_start_commands, Text(
        equals=owner.values(), ignore_case=True), state=None)
    dp.register_message_handler(create_admin, state=FSMOwner.create_admin)
    dp.register_message_handler(delete_admin, state=FSMOwner.delete_admin)
    dp.register_message_handler(show_admins, state=FSMOwner.show_admins)
