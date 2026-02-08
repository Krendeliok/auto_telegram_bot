from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship
from models import Base


class Gearbox(Base):
    __tablename__ = 'gearbox'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


    filters = relationship(
        "GearboxFilter",
        backref="gearbox"
    )

    cars = relationship(
        "Advertisement",
        backref="gearbox"
    )

    def __repr__(self):
        return f"Gearbox(id={self.id!r}, " \
               f"name={self.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
