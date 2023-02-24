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
from ..contexts import (
    FSMOwner
)
from ..keyboards import (
    clients_keyboard,
    admins_keyboard,
    commands_keyboard,
)

from .general import start_command

from ..commands import owner, special

async def owner_start_commands(message: types.Message):
    if is_owner(message.from_user.id):
        if message.text == str(owner["create_admin"]):
            await FSMOwner.create_admin.set()
            await message.answer("Оберіть юзера якого треба зробити адміном.", reply_markup=clients_keyboard(ignore_admins=True))
        elif message.text == str(owner["remove_admin"]):
            await FSMOwner.delete_admin.set()
            await message.answer("Оберіть юзера якого треба позбавити прав адміна", reply_markup=admins_keyboard())
        elif message.text == str(owner["show_admins"]):
            await FSMOwner.show_admins.set()
            await message.answer("Ось усі адміни", reply_markup=admins_keyboard())

def back_handler(previous_func, text=None):
    def wrapper(func):
        async def inner(message, state, *args, **kwargs):
            if message.text == str(special["back"]):
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
    dp.register_message_handler(owner_start_commands, Text(equals=[str(i) for i in owner.values()], ignore_case=True), state=None)
    dp.register_message_handler(create_admin, state=FSMOwner.create_admin)
    dp.register_message_handler(delete_admin, state=FSMOwner.delete_admin)
    dp.register_message_handler(show_admins, state=FSMOwner.show_admins)