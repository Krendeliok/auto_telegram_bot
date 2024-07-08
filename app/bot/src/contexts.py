from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMMenu(StatesGroup):
    contact = State()
    choose_adv = State()
    adv_action = State()

class FSMFilter(StatesGroup):
    start = State()
    producer = State()
    model = State()
    gearbox = State()
    region = State()
    engine_type = State()
    price = State()
    year = State()
    engine_volume = State()
    range = State()

class FSMAdvertisement(StatesGroup):
    producer = State()
    model = State()
    vin = State()
    price = State()
    year = State()
    engine_type = State()
    engine_volume = State()
    range = State()
    gearbox = State()
    city = State()
    description = State()
    phone_numbers = State()
    images = State()
    more_images = State()


class FSMSolution(StatesGroup):
    message = State()


class FSMAdmin(StatesGroup):
    create_model = State()
    set_producer = State()
    create_producer = State()
    create_engine = State()
    create_region = State()
    create_gearbox = State()


class FSMOwner(StatesGroup):
    create_admin = State()
    delete_admin = State()
    show_admins = State()


class FSMPayment(StatesGroup):
    menu = State()
    my_goods = State()
    choose_product = State()
    make_payment = State()