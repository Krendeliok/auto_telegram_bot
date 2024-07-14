from .texts import ADV_TEXT

import re

from aiogram.types import MediaGroup, InputMediaPhoto


def get_sending_text(data):
    return ADV_TEXT.format(
        producer=data["producer"],
        model=data["model"],
        price=data["price"],
        year=data["year"],
        engine_type=data["engine_type"],
        engine_volume=data["engine_volume"],
        range=data["range"],
        gearbox=data["gearbox_type"],
        drive_unit=data["drive_unit"],
        city=data["based_country"],
        phone_number=data["phone_number"],
        description=data["description"],
        vin=(data["vin"] if data["vin"] is not None else '—'),
        credit_price=14.5
    )


def make_advertisement(data):
    images = data["images"]
    media_group = MediaGroup()
    media_group.attach(InputMediaPhoto(images[0]["source"], caption=get_sending_text(data)))
    for image in images[1:]:
        media_group.attach(InputMediaPhoto(image["source"]))
    return media_group


def check_vin(vin):
    return re.fullmatch(r'^[A-HJ-NPR-Z0-9]{17}$', vin.upper()) is not None
