from main import bot, session
from datetime import date
from models import Advertisement, AdvertisementStateEnum
from config import CHANNEL_NAME
from aiogram.types import InputMediaPhoto, MediaGroup
import warnings

import asyncio

warnings.filterwarnings("ignore", category=DeprecationWarning) 



async def main():
    adv = (
    session.query(Advertisement)
    .filter(
        Advertisement.status == AdvertisementStateEnum.approved, 
        Advertisement.next_published_date == date.today()
    )
    .first()
    )
    if adv is not None:
        adv.update_next_date
        session.flush()
        session.commit()

        images = adv.images
        media_group = MediaGroup()
        media_group.attach(InputMediaPhoto(images[0].source, caption=adv.get_sending_text))
        for image in images[1:]:
            media_group.attach(InputMediaPhoto(image.source))
        await bot.send_media_group(
                CHANNEL_NAME,
                media=media_group
            )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    
