class Command:
    value: str

    def __init__(self, value):
        self.value = value

    @property
    def get_value(self):
        return f"{self.value}"

    def __str__(self) -> str:
        return self.get_value

    def __repr__(self) -> str:
        return self.get_value


special = {
    "end": Command("❌Скасувати"),
    "complete": Command("✅Готово"),
    "back": Command("⬅️Назад"),
    "all": Command("Усі"),
    "remove_producer": Command("❌Прибрати цю марку"),
    "find": Command("🔍Знайти"),
}

general = {
    "new_adv": Command("💵Продати машину"),
    "filter": Command("🚗Знайти машину"),
}

filters = {
    "producer": Command("Обрати марку та модель"),
    "gearbox": Command("Обрати коробку"),
    "region": Command("Обрати область"),
    "engine_type": Command("Обрати тип палива"),
    "price": Command("Встановити ціну"),
    "year": Command("Встановити рік"),
    "engine_volume": Command("Встановити об'єм двигуна"),
    "range": Command("Встановити пробіг"),
}

admin = {
    "create_producer": Command("Створити марку"),
    "create_model": Command("Створити модель"),
    "create_city": Command("Створити область"),
    "create_engine_type": Command("Створити тип палива"),
    "create_gearbox": Command("Створити коробку"),
}

owner = {
    "create_admin": Command("Створити адміна"),
    "remove_admin": Command("Видалити адміна"),
    "show_admins": Command("Показати адмінів"),
}