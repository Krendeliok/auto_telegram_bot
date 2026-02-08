from .celery_app import app
from telegram import bot

from models import Advertisement, AdvertisementStateEnum, Client
from aiogram.types import InputMediaPhoto, MediaGroup
from session import session
from src.keyboards import prolongation_keyboard, show_advertisement
from datetime import date, timedelta

import warnings

import asyncio

from config import CHANNEL_NAME

from src.Api.Request import Request

from src.queries.feedback import set_verified_feedback

# from ..models import AdvertisementKindEnum

warnings.filterwarnings("ignore", category=DeprecationWarning)

prolongate_after = {"days": 30}


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
                Advertisement.last_published_date <= date.today() - timedelta(**prolongate_after)
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

@app.task(ignore_result=True)
def new_feedbacks():
    owner = session.query(Client).filter_by(is_owner=True).first()
    if not owner:
        return
    params = {
        "verified": "false"
    }
    response = asyncio.run(Request.get("feedbacks", params=params))
    feedbacks = list(response)
    for feedback in feedbacks:
        if all((feedback["name"], feedback["phone"])):
            keyboard = None
            if feedback.get("advertisement_id"):
                keyboard = show_advertisement(feedback["advertisement_id"])
            asyncio.run(
                bot.send_message(
                    owner.telegram_id,
                    f"{feedback['name']} {feedback['phone']}",
                    reply_markup=keyboard
                )
            )
            asyncio.run(set_verified_feedback(feedback["id"]))