from api.advertisements import AdvertisementsApi, PriceApi
from api.engines import EngineApi
from api.gearboxes import GearboxApi
from api.producers import ProducersApi

def route(api):
    api.add_resource(AdvertisementsApi, "/api/v1/advertisements")
    api.add_resource(PriceApi, "/api/v1/advertisements/get_max_price")
    api.add_resource(EngineApi, "/api/v1/fuels")
    api.add_resource(GearboxApi, "/api/v1/gearboxes")
    api.add_resource(ProducersApi, "/api/v1/producers")