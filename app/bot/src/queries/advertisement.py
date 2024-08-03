from ..Api.Request import Request

from models import (
    Client,
    Advertisement,
    AdvertisementStateEnum,
    AdvertisementKindEnum,
    AditionalAdvertisements,
    Image
)
from sqlalchemy.sql import expression
from sqlalchemy import func
from session import session

from .client import get_client_by_telegram_id


def get_random_admin():
    admin = (
        session.query(Client.id, Client.telegram_id)
        .filter(Client.is_admin == expression.true())
        .order_by(func.random())
        .first()
    )
    return admin if admin else None


async def get_advertisement_by_id(id: int) -> dict:
    response = await Request.get(f"advertisements/{id}")
    return response[0]


def get_all_additional_advertisements(telegram_id) -> list[Advertisement]:
    client = get_client_by_telegram_id(telegram_id)
    return (
        session
        .query(Advertisement)
        .filter(
            Advertisement.user_id == client.id,
            Advertisement.kind == AdvertisementKindEnum.additional,
            Advertisement.status.in_([AdvertisementStateEnum.approved, AdvertisementStateEnum.draft])
        )
        .all()
    )


def count_free_additional_advertisements(telegram_id) -> int:
    client = get_client_by_telegram_id(telegram_id)
    return (
        session
        .query(AditionalAdvertisements)
        .filter(
            AditionalAdvertisements.client_id == client.id,
            AditionalAdvertisements.reserved == expression.false()
        )
        .count()
    )


def get_all_images():
    return (
        session
        .query(Image)
        .all()
    )


def set_new_image_source(image_id, new_source, new_cloudinary_source):
    image = session.query(Image).filter(Image.id == image_id).first()
    image.source = new_source
    image.cloudinary_source = new_cloudinary_source
    session.add(image)
    session.commit()


def update_adv_status(adv_id, approved: bool):
    (
        session.query(Advertisement)
        .filter(Advertisement.id == adv_id)
        .update(
            {
                'status': AdvertisementStateEnum.approved.value if approved else AdvertisementStateEnum.rejected.value
            }
        )
    )
    session.commit()


def sell_adv(adv_id):
    (
        session.query(Advertisement)
        .filter(Advertisement.id == adv_id)
        .update(
            {
                'status': AdvertisementStateEnum.sold.value
            }
        )
    )
    session.commit()


def delete_adv(adv_id):
    adv = session.query(Advertisement).filter_by(id=adv_id).first()

    session.delete(adv)
    session.commit()


def pin_admin(adv_id, admin_id):
    (
        session.query(Advertisement)
        .filter(Advertisement.id == adv_id)
        .update(
            {
                'pinned_admin_id': admin_id
            }
        )
    )
    session.commit()


def is_spam(data, telegram_id):
    client = get_client_by_telegram_id(telegram_id)

    if any([client.is_admin, client.is_owner]):
        return False

    adv = (
        session
        .query(Advertisement)
        .filter(
            Advertisement.user_id == client.id,
            Advertisement.model_id == data["model_id"],
            Advertisement.year == data["year"],
            Advertisement.engine_type_id == data["engine_type_id"],
            Advertisement.engine_volume == data["engine_volume"],
            Advertisement.gearbox_type_id == data["gearbox_type_id"],
            Advertisement.status.in_((AdvertisementStateEnum.approved, AdvertisementStateEnum.draft))
        ).first()
    )
    return bool(adv)
