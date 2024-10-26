from .celery_app import app
from telegram import bot

from models import Advertisement, AdvertisementStateEnum
from aiogram.types import InputMediaPhoto, MediaGroup
from session import session
from src.keyboards import prolongation_keyboard
from datetime import date

import warnings

import asyncio

from config import CHANNEL_NAME

# from ..models import AdvertisementKindEnum

warnings.filterwarnings("ignore", category=DeprecationWarning)


def create_media_group(adv):
    images = adv.images
    media_group = MediaGroup()
    media_group.attach(InputMediaPhoto(images[0].source, caption=adv.get_sending_text, parse_mode='html'))
    for image in images[1:]:
        media_group.attach(InputMediaPhoto(image.source))
    return media_group


@app.task(ignore_result=True)
def prolongation_advertisement_question():
    try:
        advs = (
            session.query(Advertisement)
            .filter(
                # Advertisement.kind == AdvertisementKindEnum.admin,
                Advertisement.status == AdvertisementStateEnum.approved,
                Advertisement.next_published_date <= date.today()
            )
            .all()
        )
    except Exception as e:
        print(e)
        return

    for adv in advs:
        try:
            media_group = create_media_group(adv)
            # send to adv owner with two buttons "Prolongate" and "Delete"
            asyncio.run(bot.send_media_group(
                adv.client.telegram_id,
                media=media_group
            ))
            asyncio.run(bot.send_message(
                adv.client.telegram_id,
                "Що зробити з оголошенням?",
                reply_markup=prolongation_keyboard(f'prolong:{adv.id}', f'delete:{adv.id}')
            ))
            asyncio.run(asyncio.sleep(10))
        except Exception as e:
            print(e)


@app.task(ignore_result=True)
def prolong_advertisement(adv_id):
    adv = session.query(Advertisement).get(adv_id)
    adv.update_publishing_dates()
    session.commit()
    media_group = create_media_group(adv)
    # send to channel
    asyncio.run(bot.send_media_group(
        CHANNEL_NAME,
        media=media_group
    ))


@app.task(ignore_result=True)
def delete_advertisement(adv_id):
    adv = session.query(Advertisement).get(adv_id)
    adv.status = AdvertisementStateEnum.deleted
    session.commit()
