from ..Api.Request import Request

from models import (
    CarModel,
    Client,
    Producer,
    Engine,
    Country,
    Gearbox,
    AditionalAdvertisements,
)
from sqlalchemy.sql import expression
from aiogram import types
from session import session

from .client import get_client_by_telegram_id


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
    

async def create_advertisement(data: dict):
    response = await Request.post("advertisements", body=data)
    return int(response["adv_id"])
    
def create_adittional_advertisement(telegram_id, count: int = 1):
    client = get_client_by_telegram_id(telegram_id)
    advs = [AditionalAdvertisements(
        client_id=client.id
    ) for _ in range(count)]

    session.add_all(advs)
    session.commit()
