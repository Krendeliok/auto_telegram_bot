from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship
from models import Base


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    filters = relationship(
        "RegionFilter",
        backref="region"
    )

    cars = relationship(
        "Advertisement",
        backref="country"
    )

    def __repr__(self):
        return f"Country(id={self.id!r}, " \
               f"name={self.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
