from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship
from models import Base


class Producer(Base):
    __tablename__ = 'producer'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


    filters = relationship(
        "ProducerFilter",
        backref="producer"
    )

    models = relationship(
        "CarModel",
        backref="producer"
    )

    def __repr__(self):
        return f"Producer(id={self.id!r}, " \
               f"name={self.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
