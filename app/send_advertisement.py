from aiogram.utils.exceptions import ValidationError
from time import sleep
import os

while True:
    try:
        from main import bot, session
        break
    except ValidationError:
        sleep(2) 
        print("Can`t load bot")

from datetime import date
from models import Advertisement, AdvertisementStateEnum
from config import CHANNEL_NAME
from aiogram.types import InputMediaPhoto, MediaGroup
import warnings

import asyncio

warnings.filterwarnings("ignore", category=DeprecationWarning) 

file_name = "test.log"


def create_media_group(adv):
    images = adv.images
    media_group = MediaGroup()
    media_group.attach(InputMediaPhoto(images[0].source, caption=adv.get_sending_text))
    for image in images[1:]:
        media_group.attach(InputMediaPhoto(image.source))
    return media_group

async def main():
    with open(file_name, "w") as f:
        f.write("Start sending advs")
    advs = (
        session.query(Advertisement)
        .filter(
            Advertisement.status == AdvertisementStateEnum.approved, 
            Advertisement.next_published_date <= date.today()
        )
        .all()
    )

    with open(file_name, "a") as f:
        f.write(f"Find {len(advs)} advs")

    for adv in advs:
        adv.update_publishing_dates()
        session.flush()
        session.commit()

        media_group = create_media_group(adv)

        await bot.send_media_group(
                CHANNEL_NAME,
                media=media_group
            )
        await asyncio.sleep(60)

    with open(file_name, "a") as f:
        f.write("Finish sending advs")
        

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    