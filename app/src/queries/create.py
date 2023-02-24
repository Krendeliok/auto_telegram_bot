from models import (
    CarModel,
    Client,
    Producer,
    Engine,
    Country,
    Gearbox,
    Advertisement,
    Image,
    AdvertisementKindEnum,
)
from sqlalchemy.sql import expression
from aiogram import types
from datetime import date
from ..session import session

def create_producer(name: str):
    obj = Producer(name=name)
    session.add(obj)
    session.commit()

def create_model(name: str, producer_id: int):
    obj = CarModel(name=name, producer_id=producer_id)
    session.add(obj)
    session.commit()

def create_engine_type(name: str):
    obj = Engine(name=name)
    session.add(obj)
    session.commit()

def create_city(name: str):
    obj = Country(name=name)
    session.add(obj)
    session.commit()

def create_gearbox(name: str):
    obj = Gearbox(name=name)
    session.add(obj)
    session.commit()

def create_client(data: types.Message):
    last_name = data.from_user.last_name if data.from_user.last_name else ""
    username = data.from_user.username if data.from_user.username else f"{data.from_user.first_name} {last_name}"
    client = Client(
        telegram_id=data.from_user.id,
        username=username,
        phone_number=data.contact.phone_number,
        first_name=data.from_user.first_name,
        last_name=last_name,
        is_vip=expression.false(),
        is_admin=expression.false(),
        is_owner=expression.false()
    )
    session.add(client)
    session.commit()
    

def create_advertisement(data: dict):
    user = session.query(Client).filter_by(telegram_id=data["user_id"]).first()
    data["phone"] = data.get("phone", user.phone_number)
    data["phone"] = data["phone"] if str(data["phone"]).startswith("+") else f"+{data['phone']}"
    adv = Advertisement(
        user_id=user.id,
        model_id=data["model_id"],
        price=data["price"],
        year=data["year"],
        engine_type_id=data["engine_type_id"],
        engine_volume=data["engine_volume"],
        range=data["range"],
        gearbox_type_id=data["gearbox_type_id"],
        based_country_id=data["based_country_id"],
        phone_number=data["phone"],
        description=data["description"],
        next_published_date=date.today(),
        kind=AdvertisementKindEnum.admin.value
    )
    session.add(adv)
    session.flush()
    images = [
        Image(
            advertisement_id=adv.id,
            source=image
        ) for image in data["images"]
    ]
    session.add_all(images)
    session.commit()
    return adv.id
