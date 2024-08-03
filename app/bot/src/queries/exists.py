from models import (
    CarModel,
    Client,
    Producer,
    Engine,
    Country,
    Gearbox,
    Advertisement,
    AdvertisementKindEnum,
    AdvertisementStateEnum,
    AditionalAdvertisements,
    DriveUnit,
)
from sqlalchemy.sql.expression import and_, false

from session import session

from config import VIP_ADVERTISEMENTS


def exists_producer(producer_name: str) -> tuple:
    model = session.query(Producer.id).filter(Producer.name == producer_name).first()
    return bool(model), model


def exists_model_from_producer(model_name: str, producer_name: str) -> tuple:
    model = session.query(CarModel.id).join(Producer).filter(
        and_(CarModel.name == model_name, Producer.name == producer_name)).first()
    return bool(model), model


def exists_engine_type(engine_type: str) -> tuple:
    model = session.query(Engine.id).where(Engine.name == engine_type).first()
    return bool(model), model


def exists_drive_unit(drive_unit: str) -> tuple:
    model = session.query(DriveUnit.id).where(DriveUnit.name == drive_unit).first()
    return bool(model), model


def exists_gearbox(gearbox: str) -> tuple:
    model = session.query(Gearbox.id).where(Gearbox.name == gearbox).first()
    return bool(model), model


def exists_drive_unit(drive_unit: str) -> tuple:
    model = session.query(DriveUnit.id).where(DriveUnit.name == drive_unit).first()
    return bool(model), model


def exists_city(sity_name: str) -> tuple:
    model = session.query(Country.id).where(Country.name == sity_name).first()
    return bool(model), model


def exists_client(telegram_id: int) -> tuple:
    model = session.query(Client).where(Client.telegram_id == telegram_id).first()
    return bool(model), model


def exists_adv(adv_id: int, telegram_id: int):
    adv = (
        session
        .query(Advertisement)
        .join(Client, Advertisement.user_id == Client.id)
        .filter(Client.telegram_id == telegram_id, Advertisement.id == adv_id)
        .first()
    )
    return bool(adv), adv


def exists_basic_adv(client_id: int) -> bool:
    q = (
        session
        .query(Advertisement)
        .filter(
            Advertisement.user_id == client_id,
            Advertisement.kind == AdvertisementKindEnum.basic,
            Advertisement.status.in_([AdvertisementStateEnum.draft, AdvertisementStateEnum.approved])
        )
    )
    return session.query(q.exists()).scalar()


def exists_vip_adv_space(client_id) -> bool:
    vip_advs = (
        session
        .query(Advertisement.id)
        .filter(
            Advertisement.user_id == client_id,
            Advertisement.kind == AdvertisementKindEnum.vip,
            Advertisement.status.in_([AdvertisementStateEnum.draft, AdvertisementStateEnum.approved]),
        )
        .count()
    )
    return vip_advs < int(VIP_ADVERTISEMENTS)


def exists_free_additional_adv(client_id) -> bool:
    q = (
        session
        .query(AditionalAdvertisements.id)
        .filter(
            AditionalAdvertisements.client_id == client_id,
            AditionalAdvertisements.reserved == false()
        )
    )
    return session.query(q.exists()).scalar()
