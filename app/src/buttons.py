from aiogram.types import KeyboardButton, InlineKeyboardButton

approve = lambda callback: InlineKeyboardButton("Погодити", callback_data=callback)
reject = lambda callback: InlineKeyboardButton("Відхилити", callback_data=callback)


def custom_keyboard_button(text: str):
    return KeyboardButton(text)

def custom_inline_button(text: str, callback_data: str):
    return InlineKeyboardButton(text, callback_data=callback_data)


def contact_button(text: str):
    return KeyboardButton(text, request_contact=True)

