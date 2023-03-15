from models import (
    CarModel,
    Client,
    Producer,
    Advertisement,
    AdvertisementStateEnum,
    AdvertisementKindEnum,
)

from sqlalchemy.sql.expression import and_, true, false
from datetime import date
from dateutil.relativedelta import relativedelta

from .exists import exists_basic_adv, exists_vip_adv_space, exists_free_additional_adv

from ..session import session


def is_admin(telegram_id) -> bool:
    is_admin = (
        session.query(Client.is_admin)
        .filter(
            Client.telegram_id == telegram_id           
        )
        .scalar()
    )
    return is_admin


def is_owner(telegram_id) -> bool:
    is_owner = (
        session.query(Client.is_owner)
        .filter(
            Client.telegram_id == telegram_id           
        )
        .scalar()
    )
    return is_owner


def is_vip(telegram_id) -> bool:
    is_vip = (
        session.query(Client.is_vip)
        .filter(
            Client.telegram_id == telegram_id           
        )
        .scalar()
    )
    return is_vip


def set_admin(telegram_id):
    (
        session.query(Client)
        .filter(Client.telegram_id == telegram_id)
        .update({'is_admin': true()})
    )
    session.commit()


def remove_admin(telegram_id):
    (
        session.query(Client)
        .filter(Client.telegram_id == telegram_id)
        .update({'is_admin': false()})
    )
    session.commit()


def get_client_by_username(username) -> Client:
    model = session.query(Client).filter_by(username=username).first()
    return model


def get_client_by_telegram_id(telegram_id) -> Client:
    client = session.query(Client).filter_by(telegram_id=telegram_id).first()
    return client


def client_advertisements(telegram_id) -> list[Advertisement]:
    advs = (
        session
        .query(Advertisement.id, Advertisement.year, CarModel.name, Producer.name)
        .join(Client, Advertisement.user_id == Client.id)
        .join(CarModel)
        .join(Producer)
        .filter(and_(Client.telegram_id == telegram_id, Advertisement.status == AdvertisementStateEnum.approved))
        .all()
        )
    return advs 


def get_user_phone(telegram_id) -> str:
    phone, *_ = (
        session
        .query(Client.phone_number)
        .where(Client.telegram_id == telegram_id)
        .first()
    )
    return phone


def can_create_and_kind_adv(telegram_id) -> tuple[bool, AdvertisementKindEnum | None]:
    client: Client = session.query(Client).filter_by(telegram_id=telegram_id).first()

    if any((client.is_admin, client.is_owner)):
        return (True, AdvertisementKindEnum.admin.value)
    
    if not exists_basic_adv(client.id):
        return (True, AdvertisementKindEnum.basic.value)

    if all((client.is_vip, exists_vip_adv_space(client.id))):
        return (True, AdvertisementKindEnum.vip.value)
    
    if exists_free_additional_adv(client.id):
        return (True, AdvertisementKindEnum.additional.value)

    return (False, None)


def set_vip(telegram_id, **duration):
    client: Client = (
        session.query(Client)
        .where(Client.telegram_id == telegram_id)
        .first()
    )
    if not client.is_vip:
        client.is_vip = true()
        client.vip_start = date.today()
        client.vip_end = date.today()

    client.vip_end = client.vip_end + relativedelta(**duration)
    session.commit()
