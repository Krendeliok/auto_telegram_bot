from models import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, Boolean
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship


class Filter(Base):
    __tablename__ = 'filter'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"))
    min_price = Column(Integer, default=0, server_default='0', nullable=False)
    max_price = Column(Integer, default=0, server_default='0', nullable=False)
    min_year = Column(Integer, default=0, server_default='0', nullable=False)
    max_year = Column(Integer, default=0, server_default='0', nullable=False)
    min_engine_volume = Column(Float, default=0, server_default='0', nullable=False)
    max_engine_volume = Column(Float, default=0, server_default='0', nullable=False)
    min_range = Column(Integer, default=0, server_default='0', nullable=False)
    max_range = Column(Integer, default=0, server_default='0', nullable=False)
    vin = Column(Boolean, default=expression.null(), server_default=expression.null())
    all_producers = Column(Boolean, default=expression.true(), server_default=expression.true())
    all_gearboxes = Column(Boolean, default=expression.true(), server_default=expression.true())
    all_regions = Column(Boolean, default=expression.true(), server_default=expression.true())
    all_engine_types = Column(Boolean, default=expression.true(), server_default=expression.true())

    producers = relationship(
        "ProducerFilter",
        backref="filter"
    )

    engines = relationship(
        "EngineFilter",
        backref="filter"
    )

    gearboxes = relationship(
        "GearboxFilter",
        backref="filter"
    )

    regions = relationship(
        "RegionFilter",
        backref="filter"
    )

    def __repr__(self):
        return f"Filter(id={self.id!r}, " \
               f"client={self.client.username!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
