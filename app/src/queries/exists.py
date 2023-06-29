from models import (
    CarModel,
    Client,
    Producer,
    Engine,
    Country,
    Gearbox,
    Advertisement
)
from sqlalchemy.sql.expression import and_

from ..session import session


def exists_producer(producer_name: str) -> tuple:
    model = session.query(Producer.id).filter(Producer.name == producer_name).first()
    return bool(model), model

def exists_model_from_producer(model_name: str, producer_name: str) -> tuple:
    model = session.query(CarModel.id).join(Producer).filter(and_(CarModel.name == model_name, Producer.name == producer_name)).first()
    return bool(model), model

def exists_engine_type(engine_type: str) -> tuple:
    model = session.query(Engine.id).where(Engine.name == engine_type).first()
    return bool(model), model

def exists_gearbox(gearbox: str) -> tuple:
    model = session.query(Gearbox.id).where(Gearbox.name == gearbox).first()
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
