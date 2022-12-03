class Command:
    value: str

    def __init__(self, value):
        self.value = value

    @property
    def get_command(self):
        return f"/{self.value}"

    @property
    def get_value(self):
        return f"{self.value}"

    def __str__(self) -> str:
        return self.get_value

    def __repr__(self) -> str:
        return self.get_value


special = {
    "end": Command("скасувати"),
    "complete": Command("готово"),
    "back": Command("⬅️Назад"),
    "all": Command("Усі"),
    "remove_producer": Command("❌Прибрати цю марку"),
    "find": Command("🔍Знайти"),
}

general = {
    "start": Command("start"),
    "help": Command("help"),
    "new_adv": Command("Створити_оголошення"),
    "filter": Command("Налаштувати_фільтр"),
}

filters = {
    "producer": Command("Обрати_марку_та_модель"),
    "gearbox": Command("Обрати_коробку"),
    "region": Command("Обрати_область"),
    "engine_type": Command("Обрати_тип_палива"),
    "price": Command("Встановити_ціну"),
    "year": Command("Встановити_рік"),
    "engine_volume": Command("Встановити_об'єм_двигуна"),
    "range": Command("Встановити_пробіг"),
}

admin = {
    "admin": Command("адмін"),
    "create_producer": Command("створити_марку"),
    "create_model": Command("створити_модель"),
    "create_city": Command("створити_місто"),
    "create_engine_type": Command("створити_тип_палива"),
    "create_gearbox": Command("створити_коробку"),
}

owner = {
    "owner": Command("власник"),
    "create_admin": Command("створити_адміна"),
    "remove_admin": Command("видалити_адміна"),
    "show_admins": Command("показати_адмінів"),
}