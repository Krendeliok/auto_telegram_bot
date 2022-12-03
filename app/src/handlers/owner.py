from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from ..queries import (
    is_owner,
    exists_client,
    is_admin,
    set_admin,
    remove_admin,
)
from ..contexts import (
    FSMCreateAdmin,
    FSMDeleteAdmin
)
from ..keyboards import (
    clients_keyboard,
    admins_keyboard,
    commands_keyboard,
)

from ..commands import owner, special

async def owner_start_commands(message: types.Message):
    if is_owner(message.from_user.id):
        if message.text == owner["owner"].get_command:
            await message.answer("Всі комманди", reply_markup=commands_keyboard(message.from_user.id))
        elif message.text == owner["create_admin"].get_command:
            await FSMCreateAdmin.username.set()
            await message.answer("Оберіть юзера якого треба зробити адміном.", reply_markup=clients_keyboard(ignore_admins=True))
        elif message.text == owner["remove_admin"].get_command:
            await FSMDeleteAdmin.username.set()
            await message.answer("Оберіть юзера якого треба позбавити прав адміна", reply_markup=admins_keyboard())
        elif message.text == owner["show_admins"].get_command:
            await message.answer("Ось усі адміни", reply_markup=admins_keyboard())

async def cancel_handler(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return
    await state.finish()
    await message.reply("Скасовано!", reply_markup=commands_keyboard(message.from_user.id))


async def create_admin(message: types.Message, state: FSMContext):
    exists, model = exists_client(message.from_user.id)
    if exists and not is_admin(model.telegram_id):
        set_admin(model.telegram_id)
        state.finish()
        await message.reply("Адмін успішно створений!")
    else:
        await message.reply("Я не знаю такого користувача або він вже адмін!")


async def remove_admin(message: types.Message, state: FSMContext):
    exists, model = exists_client(message.from_user.id)
    if exists and is_admin(model.telegram_id):
        remove_admin(model.telegram_id)
        state.finish()
        await message.reply("Успішно позбавлено прав адміна")
    else:
        await message.reply("Я не знаю такого користувача або він не адмін!")




def register_handlers_owner(dp: Dispatcher):
    dp.register_message_handler(owner_start_commands, commands=[str(i) for i in owner.values()])
    dp.register_message_handler(cancel_handler, state="*", commands=[str(special["end"])])
    dp.register_message_handler(cancel_handler, Text(equals=str(special["end"]), ignore_case=True), state="*")
    dp.register_message_handler(create_admin, state=FSMCreateAdmin.username)
    dp.register_message_handler(remove_admin, state=FSMDeleteAdmin.username)