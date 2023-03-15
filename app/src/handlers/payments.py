from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.types.message import ContentType

from config import PAYMENTS_TOKEN
from main import bot

from ..contexts import FSMPayment

from ..tarifs import tarifs

from ..commands import general, special

from ..keyboards import tarifs_keyboard

from ..queries.client import set_vip
from ..queries.create import create_adittional_advertisement

from .general import start_command


def add_tarif_to_user(telegram_id, tarif_id: str):
    tarif = tarifs.get(tarif_id)

    if not tarif:
        raise ValueError(f"{tarif_id=} is incorrect")

    if tarif.id.startswith("vip"):
        set_vip(telegram_id, **tarif.duration)
    elif tarif.id.endswith("_advertisement"):
        create_adittional_advertisement(telegram_id, tarif.previleges[0].count)


def inline_back_handler(previous_func, text=None):
    def wrapper(func):
        async def inner(callback_query: CallbackQuery, state, *args, **kwargs):
            if callback_query.data == "back":
                await previous_func(callback_query.message, state, *args, **kwargs)
                await callback_query.message.delete()
                return
            await func(callback_query, state)
        return inner
    return wrapper


async def buy_handler(message: Message, state: FSMContext, **kwargs):
    if kwargs.get("after_success", False):
        await message.answer("Хочете купити щось ще?", reply_markup=tarifs_keyboard())
    else:
        await message.answer("Оберіть товар", reply_markup=tarifs_keyboard())
    await state.set_state(FSMPayment.choose_product)


@inline_back_handler(start_command)
async def send_payment(callback_query: CallbackQuery, state: FSMContext, **kwargs):
    tarif_id = callback_query.data.split(":")[1]
    tarif = tarifs.get(tarif_id)
    labeled_price = [LabeledPrice(tarif.title, tarif.price)]
    await callback_query.message.bot.send_invoice(
        callback_query.message.chat.id,
        title=tarif.title,
        description=tarif.description,
        provider_token=PAYMENTS_TOKEN,
        currency="uah",
        prices=labeled_price,
        need_email=True,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=False,
        start_parameter=tarif_id,
        payload=tarif_id
    )
    await state.set_state(FSMPayment.make_payment)


async def checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def success_payment(message: Message, state: FSMContext):
    try:
        add_tarif_to_user(message.from_user.id, message.successful_payment.invoice_payload)
        tarif = tarifs.get(message.successful_payment.invoice_payload)
    except ValueError:
        await message.answer("Щось пішло не так")
        return

    await message.answer(f"✅Дякуємо за покупку '{tarif.title}'")
    await buy_handler(message, state, after_success=True)


def register_hendlers_payment(dp: Dispatcher):
    dp.register_message_handler(buy_handler, Text(equals=str(general["payment"])), state="*")
    dp.register_callback_query_handler(send_payment, state=FSMPayment.choose_product)
    dp.register_pre_checkout_query_handler(checkout_handler, lambda q: True, state=FSMPayment.make_payment)
    dp.register_message_handler(success_payment, content_types=ContentType.SUCCESSFUL_PAYMENT, state="*")
