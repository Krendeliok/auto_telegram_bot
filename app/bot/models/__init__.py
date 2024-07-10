from sqlalchemy.orm import configure_mappers

from models.base import Base

from .advertisement import Advertisement, AdvertisementStateEnum, AdvertisementKindEnum
from .additional_advertisements import AditionalAdvertisements
from .client import Client
from .engine import Engine
from .car_model import CarModel
from .gearbox import Gearbox
from .producer import Producer
from .country import Country
from .image import Image
from .filter import Filter
from .engine_filter import EngineFilter
from .model_filter import ModelFilter
from .region_filter import RegionFilter
from .gearbox_filter import GearboxFilter
from .producer_filter import ProducerFilter
from .drive_unit import DriveUnit
from .drive_unit_filter import DriveUnitFilter

configure_mappers()
