from models import (
    CarModel,
    Client,
    Producer,
    Engine,
    Country,
    Gearbox,
    Advertisement,
    Image,
    AdvertisementStateEnum,
    Filter,
    ModelFilter,
    EngineFilter,
    RegionFilter,
    GearboxFilter,
    ProducerFilter
)
from sqlalchemy import (
    select,
    insert,
    update,
    and_
)
from sqlalchemy.sql import expression
from sqlalchemy.sql.expression import or_, and_
from aiogram import types
from datetime import date

from .session import session

from random import choice


def exists_producer(producer_name: str) -> tuple:
    model = select(Producer.id).where(Producer.name == producer_name).execute().first()
    return bool(model), model

def exists_model_from_producer(model_name: str, producer_name: str) -> tuple:
    model = select(CarModel.id).join(Producer).filter(and_(CarModel.name == model_name, Producer.name == producer_name)).execute().first()
    return bool(model), model

def exists_engine_type(engine_type: str) -> tuple:
    model = select(Engine.id).where(Engine.name == engine_type).execute().first()
    return bool(model), model

def exists_gearbox(gearbox: str) -> tuple:
    model = select(Gearbox.id).where(Gearbox.name == gearbox).execute().first()
    return bool(model), model

def exists_city(sity_name: str) -> tuple:
    model = select(Country.id).where(Country.name == sity_name).execute().first()
    return bool(model), model

def exists_client(telegram_id: int) -> tuple:
    model = select(Client).where(Client.telegram_id == telegram_id).execute().first()
    return bool(model), model


def create_producer(name: str):
    obj = (
        insert(Producer)
        .values(name=name)
        .execute()
    )
    return obj

def create_model(name: str, producer_id: int):
    obj = (
        insert(CarModel)
        .values(
            name=name,
            producer_id=producer_id
        )
        .execute()
    )
    return obj

def create_engine_type(name: str):
    obj = (
        insert(Engine)
        .values(name=name)
        .execute()
    )
    return obj

def create_city(name: str):
    obj = (
        insert(Country)
        .values(name=name)
        .execute()
    )
    return obj

def create_gearbox(name: str):
    obj = (
        insert(Gearbox)
        .values(name=name)
        .execute()
    )
    return obj


def create_client(data: types.Message):
    last_name = data.from_user.last_name if data.from_user.last_name else ""
    username = data.from_user.username if data.from_user.username else f"{data.from_user.first_name} {last_name}"
    obj = (
        insert(Client)
        .values(
            telegram_id=data.from_user.id,
            username=username,
            phone_number=data.contact.phone_number,
            first_name=data.from_user.first_name,
            last_name=last_name,
            is_vip=expression.false(),
            is_admin=expression.false(),
            is_owner=expression.false()
        ).execute()
    )
    return obj

def create_advertisement(data: dict):
    user_id, *_ = select(Client.id).where(Client.telegram_id == data["user_id"]).execute().first()
    adv = (
        insert(Advertisement)
        .values(
            user_id=user_id,
            model_id=data["model_id"],
            price=data["price"],
            year=data["year"],
            engine_type_id=data["engine_type_id"],
            engine_volume=data["engine_volume"],
            range=data["range"],
            gearbox_type_id=data["gearbox_type_id"],
            based_country_id=data["based_country_id"],
            description=data["description"],
            next_published_date=date.today()
        )
        .execute()
    )
    
    for image in data["images"]:
        (
            insert(Image)
            .values(
                advertisement_id=adv.inserted_primary_key["id"],
                source=image
            )
            .execute()
        )
    return adv.inserted_primary_key["id"]

def get_random_admin():
    admins = select(Client.telegram_id, Client.id).filter(Client.is_admin == expression.true()).execute().fetchall()
    return choice(admins)

def get_advertisement(id) -> Advertisement:
    return session.query(Advertisement).where(Advertisement.id == id).first()

def update_adv_status(adv_id, approved: bool):
    adv = (
        update(Advertisement)
        .where(Advertisement.id == adv_id)
        .values(
            status=AdvertisementStateEnum.approved.value if approved else AdvertisementStateEnum.rejected.value
        ).execute()
    )
    return adv

def pin_admin(adv_id, admin_id):
    obj = (
        update(Advertisement)
        .where(Advertisement.id == adv_id)
        .values(pinned_admin_id = admin_id)
        .execute()
    )
    return obj

def is_admin(telegram_id):
    obj = (
        select(Client)
        .where(
            and_(
                Client.telegram_id == telegram_id, 
                Client.is_admin == expression.true()
            )            
        )
        .execute()
        .first()
    )
    return bool(obj)

def is_owner(telegram_id):
    obj = (
        select(Client)
        .where(
            and_(
                Client.telegram_id == telegram_id, 
                Client.is_owner == expression.true()
            )            
        )
        .execute()
        .first()
    )
    return bool(obj)

def set_admin(telegram_id):
    obj = (
        update(Client)
        .where(Client.telegram_id == telegram_id)
        .values(is_admin = expression.true())
        .execute()
    )
    return obj

def remove_admin(telegram_id):
    obj = (
        update(Client)
        .where(Client.telegram_id == telegram_id)
        .values(is_admin = expression.false())
        .execute()
    )
    return obj

def get_or_create(model, delete_if_exists=False, **kwargs):
    instance = session.query(model).filter_by(**kwargs)
    created = False
    if not instance.first():
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        created = True
    elif delete_if_exists:
        instance.delete()
    else:
        instance = instance.first()
    return created, instance

def get_user_filter(telegram_id) -> Filter:
    client = session.query(Client).where(Client.telegram_id == telegram_id).first()
    return get_or_create(Filter, user_id=client.id)[1]

def add_filter_producer(user_filter: Filter, producer_id=None, set_all=False):
    user_filter.all_producers = expression.true() if set_all else expression.false()
    session.commit()
    if not set_all:
        producer_filter = get_or_create(ProducerFilter, producer_id=producer_id, filter_id=user_filter.id)[1]
        return producer_filter
    else:
        session.query(ProducerFilter).where(ProducerFilter.filter_id == user_filter.id).delete()
        session.commit()

def add_filter_model(producer_filter_id: int, model_id=None, set_all=False, delete_if_exists=True):
    producer_filter = session.get(ProducerFilter, producer_filter_id)
    producer_filter.all_models = expression.true() if set_all else expression.false()
    session.commit()
    if not set_all:
        model_filter = get_or_create(ModelFilter, delete_if_exists, model_id=model_id, producer_filter_id=producer_filter_id)
        return model_filter
    else:
        session.query(ModelFilter).where(ModelFilter.producer_filter_id == producer_filter_id).delete()
        session.commit()

def add_filter_gearbox(user_filter: Filter, gearbox_id=None, set_all=False, delete_if_exists=True):
    user_filter.all_gearboxes = expression.true() if set_all else expression.false()
    session.commit()
    if not set_all:
        gearbox_filter = get_or_create(GearboxFilter, delete_if_exists, gearbox_id=gearbox_id, filter_id=user_filter.id)
        return gearbox_filter
    else:
        session.query(GearboxFilter).where(GearboxFilter.filter_id == user_filter.id).delete()
        session.commit()

def add_filter_region(user_filter: Filter, region_id=None, set_all=False, delete_if_exists=True):
    user_filter.all_regions = expression.true() if set_all else expression.false()
    session.commit()
    if not set_all:
        region_filter = get_or_create(RegionFilter, delete_if_exists, region_id=region_id, filter_id=user_filter.id)
        return region_filter
    else:
        session.query(RegionFilter).where(RegionFilter.filter_id == user_filter.id).delete()
        session.commit()

def add_filter_engine(user_filter: Filter, engine_id=None, set_all=False, delete_if_exists=True):
    user_filter.all_engine_types = expression.true() if set_all else expression.false()
    session.commit()
    if not set_all:
        engine_filter = get_or_create(EngineFilter, delete_if_exists, engine_id=engine_id, filter_id=user_filter.id)
        return engine_filter
    else:
        session.query(EngineFilter).where(EngineFilter.filter_id == user_filter.id).delete()
        session.commit()

def add_filter_price(user_filter: Filter, min_value, max_value):
    user_filter.min_price = min_value or 0
    user_filter.max_price = max_value or 0
    session.commit()

def add_filter_range(user_filter: Filter, min_value, max_value):
    user_filter.min_range = min_value or 0
    user_filter.max_range = max_value or 0
    session.commit()

def add_filter_year(user_filter: Filter, min_value, max_value):
    user_filter.min_year = min_value or 0
    user_filter.max_year = max_value or 0
    session.commit()

def add_filter_engine_volume(user_filter: Filter, min_value, max_value):
    user_filter.min_engine_volume = min_value or 0
    user_filter.max_engine_volume = max_value or 0
    session.commit()

def remove_producer_from_filter(user_filter_id, producer_name):
    pf = session.query(ProducerFilter.id).join(Producer).join(Filter).filter(
        and_(
            Producer.name == producer_name,
            Filter.id == user_filter_id
        )
    ).first()
    session.query(ProducerFilter).filter(ProducerFilter.id == pf.id).delete()
    session.commit()

def get_advertisements_by_filter(user_filter: Filter):
    advertisements = session.query(Advertisement)
    statements = []
    if user_filter.all_producers == expression.false() and len(user_filter.producers) > 0:
        producer_ids = []
        models_ids = []
        for producer_filter in user_filter.producers:
            if producer_filter.all_models == expression.false() and len(producer_filter.models_filter) > 0:
                models_ids += [model_filter.model_id for model_filter in producer_filter.models_filter]
            else:
                producer_ids.append(producer_filter.producer_id)
        
        advertisements = advertisements.join(CarModel)
        if all([producer_ids, models_ids]):
            statements.append(or_(CarModel.producer_id.in_(producer_ids), Advertisement.model_id.in_(models_ids)))
        elif any([producer_ids, models_ids]):
            statements.append(CarModel.producer_id.in_(producer_ids) if producer_ids else Advertisement.model_id.in_(models_ids))
    
    if user_filter.all_gearboxes == expression.false() and len(user_filter.gearboxes) > 0:
        statements.append(Advertisement.gearbox_type_id.in_((gearbox.gearbox_id for gearbox in user_filter.gearboxes)))

    if user_filter.all_engine_types == expression.false() and len(user_filter.engines) > 0:
        statements.append(Advertisement.engine_type_id.in_((engine.engine_id for engine in user_filter.engines)))

    if user_filter.all_regions == expression.false() and len(user_filter.regions) > 0:
        statements.append(Advertisement.based_country_id.in_((region.region_id for region in user_filter.regions)))
    
    if user_filter.min_price != 0:
        statements.append(Advertisement.price >= user_filter.min_price)

    if user_filter.min_year != 0:
        statements.append(Advertisement.year >= user_filter.min_year)

    if user_filter.min_range != 0:
        statements.append(Advertisement.range >= user_filter.min_range)

    if user_filter.min_engine_volume != 0:
        statements.append(Advertisement.engine_volume >= user_filter.min_engine_volume)
    
    if user_filter.max_price != 0:
        statements.append(Advertisement.price <= user_filter.max_price)

    if user_filter.max_year != 0:
        statements.append(Advertisement.year <= user_filter.max_year)

    if user_filter.max_range != 0:
        statements.append(Advertisement.range <= user_filter.max_range)
    
    if user_filter.max_engine_volume != 0:
        statements.append(Advertisement.engine_volume <= user_filter.max_engine_volume)

    advertisements = advertisements.where(Advertisement.status == AdvertisementStateEnum.approved.value, *statements).all()
    return advertisements

def get_client_by_username(username):
    model = select(Client).where(Client.username == username).execute().first()
    return bool(model), model
