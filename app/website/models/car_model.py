from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from models import Base


class CarModel(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    producer_id = Column(Integer, ForeignKey("producer.id"), nullable=False)
    name = Column(String, nullable=False)


    filters = relationship(
        "ModelFilter",
        backref="model"
    )

    cars = relationship(
        "Advertisement",
        backref="model"
    )

    def __repr__(self):
        return f"CarModel(id={self.id!r}, " \
               f"producer={self.producer.name!r}, " \
               f"name={self.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
