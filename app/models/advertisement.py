from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Float,
    Text,
    Enum,
    Date,
)
from sqlalchemy.orm import relationship
import enum
from models import Base
from datetime import date
from dateutil.relativedelta import relativedelta

from src.texts import ADV_TEXT


class AdvertisementStateEnum(enum.Enum):
    approved = "approved"
    rejected = "rejected"
    draft = "draft"
    sold = "sold"


class Advertisement(Base):
    __tablename__ = 'adv'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"))
    model_id = Column(Integer, ForeignKey("model.id", ondelete="SET NULL"))
    price = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    engine_type_id = Column(Integer, ForeignKey("engine.id", ondelete="SET NULL"))
    engine_volume = Column(Float, nullable=False)
    range = Column(Integer, nullable=False)
    gearbox_type_id = Column(Integer, ForeignKey("gearbox.id", ondelete="SET NULL"))
    based_country_id = Column(Integer, ForeignKey("country.id", ondelete="SET NULL"))
    phone_number = Column(String)
    description = Column(Text, nullable=False)
    status = Column(
        Enum(AdvertisementStateEnum, values_callable=lambda obj: [e.value for e in obj]), 
        default=AdvertisementStateEnum.draft.value,
        server_default=AdvertisementStateEnum.draft.value,
        nullable=False
        )
    pinned_admin_id = Column(Integer, ForeignKey("client.id", ondelete="SET NULL"))
    last_published_date = Column(Date, default=date.today())
    next_published_date = Column(Date)


    images = relationship(
        "Image",
        backref="advertisement"
    )

    @property
    def get_sending_text(self):
        return ADV_TEXT.format(
            producer=self.model.producer.name, model=self.model.name, price=self.price, year=self.year, engine_volume=self.engine_volume, 
            engine_type=self.engine.name, gearbox=self.gearbox.name,
            range=self.range, city=self.country.name, 
            phone_number=self.phone_number if self.phone_number else self.client.phone_number, description=self.description
        )

    @property
    def update_next_date(self):
        self.last_published_date = date.today()
        self.next_published_date = date.today() + relativedelta(months=+1)

    def __repr__(self):
        return f"Advertisement(id={self.id!r}, " \
               f"model={self.model.id!r}, " \
               f"client={self.client.username!r}, "\
               f"status={self.status})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
