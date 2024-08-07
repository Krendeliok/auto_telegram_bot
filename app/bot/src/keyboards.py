from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup
from sqlalchemy.sql import expression
from sqlalchemy.sql.expression import and_

from .buttons import (
    approve,
    reject,
    custom_keyboard_button,
    custom_inline_button,
    contact_button,
)

from sqlalchemy import (
    select,
)

from .commands import general, admin, owner, filters, special, payments, vin
from .queries.client import client_advertisements
from .queries.advertisement import get_all_additional_advertisements
from .queries.exists import exists_client
from session import session

from models import (
    Producer,
    CarModel,
    Engine,
    Country,
    Gearbox,
    Client,
    Filter,
    DriveUnit,
    ProducerFilter,
    ModelFilter,
    EngineFilter,
    RegionFilter,
    GearboxFilter,
    DriveUnitFilter
)

from .tarifs import tarifs


# region base
def inline_keyboard(row_width=3):
    def wrapper(func):
        def inner(*args, **kwargs):
            keyboard = InlineKeyboardMarkup(row_width=row_width)
            func(keyboard, *args, **kwargs)
            return keyboard

        return inner

    return wrapper


def reply_keyboard(resize_keyboard=True, row_width=3):
    def wrapper(func):
        def inner(*args, **kwargs):
            keyboard = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=row_width)
            func(keyboard, *args, **kwargs)
            return keyboard

        return inner

    return wrapper


def add_user_filter():
    def wrapper(func):
        def inner(keyboard, telegram_id=None, *args, **kwargs):
            object_filter = None
            if telegram_id is not None:
                object_filter = (
                    session
                    .query(
                        Filter.id,
                        Filter.all_producers,
                        Filter.all_gearboxes,
                        Filter.all_engine_types,
                        Filter.all_regions,
                        Filter.all_drive_units
                    )
                    .join(Client)
                    .filter(Client.telegram_id == telegram_id)
                    .first()
                )
            func(keyboard=keyboard, object_filter=object_filter, telegram_id=telegram_id, *args, **kwargs)
            return keyboard

        return inner

    return wrapper


def add_producer_filter():
    def wrapper(func):
        def inner(keyboard, telegram_id=None, producer_name=None, *args, **kwargs):
            object_filter = None
            if all((telegram_id, producer_name)):
                object_filter = (
                    session
                    .query(ProducerFilter.id, ProducerFilter.all_models)
                    .join(Producer)
                    .join(Filter)
                    .join(Client)
                    .filter(and_(Client.telegram_id == telegram_id, Producer.name == producer_name))
                    .first()
                )
            func(keyboard=keyboard, object_filter=object_filter, telegram_id=telegram_id, producer_name=producer_name,
                 *args, **kwargs)
            return keyboard

        return inner

    return wrapper


def add_back_button(func):
    def wrapper(keyboard: ReplyKeyboardMarkup, *args, **kwargs):
        keyboard.add(custom_keyboard_button(special["back"]))
        func(keyboard, *args, **kwargs)
        return keyboard

    return wrapper


def add_inline_back_button(func):
    def wrapper(keyboard: InlineKeyboardMarkup, *args, **kwargs):
        keyboard.add(custom_inline_button(special["back"], "back"))
        func(keyboard, *args, **kwargs)
        return keyboard

    return wrapper


def filter_keyboard(col_name=""):
    def wrapper(func):
        def inner(keyboard, object_filter, *args, **kwargs):
            no_end = kwargs.get("no_end")
            is_filter = False
            if kwargs.pop("filter_buttons", False):
                is_filter = True
                keyboard.insert(
                    custom_keyboard_button(f"{special['all']}{'✅' if getattr(object_filter, col_name) else ''}")
                )
                if "producer_name" in kwargs:
                    keyboard.add(
                        custom_keyboard_button(special["remove_producer"])
                    )
            if not is_filter and not no_end:
                keyboard.insert(custom_keyboard_button(special["end"]))
            func(keyboard=keyboard, is_filter=is_filter, object_filter=object_filter, *args, **kwargs)
            return keyboard

        return inner

    return wrapper


def get_additinig(all_object):
    if all_object is None:
        return ""
    if all_object:
        return "✅"
    return "🟠"


def add_objects_to_keyboard(keyboard: ReplyKeyboardMarkup, objects: list, is_filter=False):
    obj_add = ""
    if is_filter:
        obj_add = get_additinig(objects[0].all_object)
    keyboard.add(custom_keyboard_button(f"{objects[0].name}{obj_add}"))
    for object in objects[1:]:
        if is_filter:
            obj_add = get_additinig(object.all_object)
        keyboard.insert(custom_keyboard_button(f"{object.name}{obj_add}"))


@reply_keyboard()
def filter_buttons(keyboard):
    keyboard.row(custom_keyboard_button(special["back"]), custom_keyboard_button(special["all"]))


@reply_keyboard()
def contact_keyboard(keyboard):
    keyboard.add(contact_button("Поділитись контактом"))


@reply_keyboard(row_width=2)
def commands_keyboard(keyboard, telegram_id=None):
    commands: list = list(general.values())
    if telegram_id is not None:
        _, model = exists_client(telegram_id)
        if model.is_admin:
            commands += list(admin.values())
        if model.is_owner:
            commands += list(owner.values())

    for command in commands:
        keyboard.insert(custom_keyboard_button(command))


def hide_keyboard():
    return ReplyKeyboardRemove()


@reply_keyboard(row_width=2)
@add_back_button
def filter_commands(keyboard):
    keyboard.insert(custom_keyboard_button(special["find"]))
    for command in filters.values():
        keyboard.insert(custom_keyboard_button(command))


@reply_keyboard()
def back_complete_keyboard(keyboard, complete=False, deny=False, skip=False):
    keyboard.add(custom_keyboard_button(special["back"]))
    if skip:
        keyboard.insert(custom_keyboard_button(special["skip"]))
    if complete:
        keyboard.insert(custom_keyboard_button(special["complete"]))
    if deny:
        keyboard.insert(custom_keyboard_button(special["end"]))


@reply_keyboard()
@add_back_button
def phone_numbers_keyboard(keyboard):
    keyboard.row(custom_keyboard_button(special["private_phone"]), custom_keyboard_button(special["comercial_phone"]))


# endregion

# region models_keyboards
@reply_keyboard()
@add_user_filter()
@add_back_button
@filter_keyboard(col_name="all_producers")
def producers_keyboard(keyboard, is_filter, object_filter, **kwargs):
    if not is_filter:
        producers = (
            session
            .query(
                Producer.name
            )
        )
    else:
        producers = (
            session
            .query(
                Producer.name,
                ProducerFilter.all_models.label("all_object")
            )
            .outerjoin(
                ProducerFilter,
                and_(
                    ProducerFilter.filter_id == object_filter.id,
                    ProducerFilter.producer_id == Producer.id
                )
            )
        )
    producers = producers.all()
    add_objects_to_keyboard(keyboard, producers, is_filter)


@reply_keyboard()
@add_producer_filter()
@add_back_button
@filter_keyboard(col_name="all_models")
def models_keyboard(keyboard, producer_name, is_filter, object_filter, **kwargs):
    if not is_filter:
        models = (
            session
            .query(
                CarModel.name
            )
            .join(Producer)
            .filter(Producer.name == producer_name)
        )
    else:
        models = (
            session
            .query(
                CarModel.name,
                ModelFilter.producer_filter_id.label("all_object")
            )
            .join(
                Producer,
                Producer.id == CarModel.producer_id
            ).outerjoin(
                ModelFilter,
                and_(
                    ModelFilter.model_id == CarModel.id,
                    ModelFilter.producer_filter_id == object_filter.id
                )
            )
            .where(Producer.name == producer_name)
        )
    models = models.all()
    add_objects_to_keyboard(keyboard, models, is_filter)


@reply_keyboard()
@add_user_filter()
@add_back_button
@filter_keyboard(col_name="all_engine_types")
def engine_keyboard(keyboard, is_filter, object_filter, **kwargs):
    if not is_filter:
        engines = (
            session
            .query(
                Engine.name,
            )
        )
    else:
        engines = (
            session
            .query(Engine.name, EngineFilter.filter_id.label("all_object"))
            .outerjoin(
                EngineFilter,
                and_(
                    EngineFilter.engine_id == Engine.id,
                    EngineFilter.filter_id == object_filter.id
                )
            )
        )
    engines = engines.all()
    add_objects_to_keyboard(keyboard, engines, is_filter)


@reply_keyboard()
@add_user_filter()
@add_back_button
def vin_keyboard(keyboard, **kwargs):
    keyboard.insert(custom_keyboard_button(vin["any"]))
    keyboard.insert(custom_keyboard_button(vin["with_vin"]))
    keyboard.insert(custom_keyboard_button(vin["without_vin"]))


@reply_keyboard()
@add_user_filter()
@add_back_button
@filter_keyboard(col_name="all_gearboxes")
def gearbox_keyboard(keyboard, is_filter, object_filter, **kwargs):
    if not is_filter:
        gearboxes = (
            session
            .query(
                Gearbox.name
            )
        )
    else:
        gearboxes = (
            session
            .query(Gearbox.name, GearboxFilter.filter_id.label("all_object"))
            .outerjoin(
                GearboxFilter,
                and_(
                    GearboxFilter.gearbox_id == Gearbox.id,
                    GearboxFilter.filter_id == object_filter.id
                )
            )
        )
    gearboxes = gearboxes.all()
    add_objects_to_keyboard(keyboard, gearboxes, is_filter)


@reply_keyboard()
@add_user_filter()
@add_back_button
@filter_keyboard(col_name="all_drive_units")
def drive_unit_keyboard(keyboard, is_filter, object_filter, **kwargs):
    if not is_filter:
        drive_units = (
            session
            .query(
                DriveUnit.name
            )
        )
    else:
        drive_units = (
            session
            .query(DriveUnit.name, DriveUnitFilter.filter_id.label("all_object"))
            .outerjoin(
                DriveUnitFilter,
                and_(
                    DriveUnitFilter.drive_unit_id == DriveUnit.id,
                    DriveUnitFilter.filter_id == object_filter.id
                )
            )
        )
    drive_units = drive_units.all()
    add_objects_to_keyboard(keyboard, drive_units, is_filter)


@reply_keyboard()
@add_user_filter()
@add_back_button
@filter_keyboard(col_name="all_regions")
def country_keyboard(keyboard, is_filter, object_filter, **kwargs):
    if not is_filter:
        countries = (
            session
            .query(
                Country.name
            )
        )
    else:
        countries = (
            session
            .query(Country.name, RegionFilter.filter_id.label("all_object"))
            .outerjoin(
                RegionFilter,
                and_(
                    RegionFilter.region_id == Country.id,
                    RegionFilter.filter_id == object_filter.id
                )
            )
        )
    countries = countries.all()
    add_objects_to_keyboard(keyboard, countries, is_filter)


@inline_keyboard(row_width=2)
@add_inline_back_button
def client_advertisements_keyboard(keyboard, telegram_id):
    advs = client_advertisements(telegram_id)
    for (id, year, model, producer) in advs:
        keyboard.insert(custom_inline_button(f"{producer} {model} {year}", f"adv_id:{id}"))


@inline_keyboard()
@add_inline_back_button
def adv_action_keyboard(keyboard):
    keyboard.insert(custom_inline_button(special["sold"], "sold"))
    keyboard.insert(custom_inline_button(special["remove"], "remove"))


# endregion

# region owner
@reply_keyboard()
@add_back_button
def clients_keyboard(keyboard, ignore_admins=False):
    clients = select(Client)
    if ignore_admins:
        clients = clients.where(Client.is_admin == expression.false())
    clients = clients.execute().fetchall()
    for client in clients:
        keyboard.insert(custom_keyboard_button(client.username))


@reply_keyboard()
@add_back_button
def admins_keyboard(keyboard):
    admins = select(Client).where(Client.is_admin == expression.true()).execute().fetchall()
    for adm in admins:
        keyboard.insert(custom_keyboard_button(adm.username))


@inline_keyboard()
def show_advertisement(keyboard: InlineKeyboardMarkup, adv_id: int):
    keyboard.add(custom_inline_button("Подивитись оголошення", f"show_adv:{adv_id}"))


# endregion

# region advertisement
@inline_keyboard()
def adverisement_keyboard(keyboard: InlineKeyboardMarkup, approve_text, reject_text):
    keyboard.add(approve(approve_text), reject(reject_text))


@inline_keyboard()
def prolongation_keyboard(keyboard: InlineKeyboardMarkup, prolongate_text, delete_text):
    keyboard.add(custom_inline_button("Продовжити", prolongate_text))
    keyboard.add(custom_inline_button("Видалити", delete_text))


# endregion

# region payments

@inline_keyboard(row_width=2)
@add_inline_back_button
def tarifs_keyboard(keyboard: InlineKeyboardMarkup):
    for id, tarif in tarifs.items():
        keyboard.insert(custom_inline_button(f"{tarif.title}", f"tarif:{id}"))


@inline_keyboard(row_width=2)
def decline_invoice_keyboard(keyboard: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    keyboard.add(custom_inline_button("Купити", None, pay_button=True))
    keyboard.insert(custom_inline_button(special["back"], "cancel_payment"))


@reply_keyboard(row_width=2)
@add_back_button
def paymets_keyboard(keyboard: ReplyKeyboardMarkup):
    for command in payments.values():
        keyboard.insert(custom_keyboard_button(command))


@inline_keyboard(row_width=2)
@add_inline_back_button
def goods_keyboard(keyboard: InlineKeyboardMarkup, telegram_id, vip: bool = False):
    if vip:
        keyboard.insert(custom_inline_button("Вип", "my_vip"))
    advs = get_all_additional_advertisements(telegram_id)
    for adv in advs:
        keyboard.add(custom_inline_button(f"{adv.model.producer.name} {adv.model.name} {adv.year}", f"adv:{adv.id}"))

# endregion
