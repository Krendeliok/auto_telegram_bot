from models import (
    Client,
    Advertisement,
    AdvertisementStateEnum,
)
from sqlalchemy.sql import expression
from sqlalchemy import func
from ..session import session

from .client import get_client_by_telegram_id



def get_random_admin():
    admin = (
        session.query(Client.id, Client.telegram_id)
        .filter(Client.is_admin == expression.true())
        .order_by(func.random())
        .first()
    )
    return admin if admin else None


def get_advertisement(id) -> Advertisement:
    return session.query(Advertisement).filter_by(id=id).first()


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
