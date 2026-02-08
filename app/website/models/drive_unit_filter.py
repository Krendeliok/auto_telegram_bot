from models import Base
from sqlalchemy import Column, ForeignKey, Integer


class DriveUnitFilter(Base):
    __tablename__ = 'drive_unit_filter'
    id = Column(Integer, primary_key=True)
    filter_id = Column(Integer, ForeignKey("filter.id", ondelete="CASCADE"))
    drive_unit_id = Column(Integer, ForeignKey("drive_unit.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"DriveUnitFilter(id={self.id!r}, " \
               f"drive_unit={self.drive_unit.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
