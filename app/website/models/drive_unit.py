from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship
from models import Base


class DriveUnit(Base):
    __tablename__ = 'drive_unit'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    filters = relationship(
        "DriveUnitFilter",
        backref="drive_unit"
    )

    cars = relationship(
        "Advertisement",
        backref="drive_unit"
    )

    def __repr__(self):
        return f"DriveUnit(id={self.id!r}, " \
               f"name={self.name!r})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
