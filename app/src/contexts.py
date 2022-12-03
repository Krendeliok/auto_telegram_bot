from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdvertisement(StatesGroup):
    producer = State()
    model = State()
    price = State()
    year = State()
    engine_type = State()
    engine_volume = State()
    range = State()
    gearbox = State()
    city = State()
    description = State()
    images = State()
    more_images = State()


class FSMContact(StatesGroup):
    contact = State()


class FSMSolution(StatesGroup):
    message = State()


class FSMCreateModel(StatesGroup):
    model_name = State()
    producer = State()


class FSMCreateProducer(StatesGroup):
    producer_name = State()


class FSMCreateEngineType(StatesGroup):
    engine_name = State()


class FSMCreateCity(StatesGroup):
    city_name = State()


class FSMCreateGearbox(StatesGroup):
    gearbox_name = State()


class FSMCreateAdmin(StatesGroup):
    username = State()


class FSMDeleteAdmin(StatesGroup):
    username = State()


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
