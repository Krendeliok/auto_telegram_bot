from dataclasses import dataclass, field


@dataclass(init=False)
class Previlege:
    name = ""
    count: int


@dataclass
class AdvertisementPrevilege(Previlege):
    name = "advertisement"


@dataclass
class SearchPrevilege(Previlege):
    name = "search"


@dataclass
class TarifDetail:
    id: str
    title: str
    description: str
    price: int
    duration: dict[str: int]
    previleges: list[Previlege]

    def __post_init__(self):
        self.price *= 100



tarifs = {
    "vip": TarifDetail(
        "vip", 
        "Віп", 
        "Віп +1 місяць", 
        200, 
        {
            "months": +1
        }, 
        [AdvertisementPrevilege(10), SearchPrevilege(5)]
    ),
    "vip3": TarifDetail(
        "vip3", 
        "Віп+", 
        "Віп +3 місяць", 
        500, 
        {
            "months": +3
        }, 
        [AdvertisementPrevilege(10), SearchPrevilege(5)]
    ),
    "addition_advertisement": TarifDetail(
        "addition_advertisement", 
        "Оголошення", 
        "Додаткове оголошення", 
        30, 
        {
            "months": +1
        }, 
        [AdvertisementPrevilege(1)]
    ),
    "addition_search": TarifDetail(
        "addition_search", 
        "Підписка", 
        "Додаткова підписка на нові оголошення", 
        30, 
        {
            "months": +1
        }, 
        [SearchPrevilege(1)]
    )
}