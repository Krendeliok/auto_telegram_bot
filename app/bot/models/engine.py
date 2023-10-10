from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship
from models import Base


class Engine(Base):
    __tablename__ = 'engine'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    filters = relationship(
        "EngineFilter",
        backref="engine"
    )

    cars = relationship(
        "Advertisement",
        backref="engine"
    )

    def __repr__(self):
        return f"Producer(id={self.id!r}, " \
               f"name={self.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
