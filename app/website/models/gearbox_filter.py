from models import Base
from sqlalchemy import Column, ForeignKey, Integer


class GearboxFilter(Base):
    __tablename__ = 'gearbox_filter'
    id = Column(Integer, primary_key=True)
    filter_id = Column(Integer, ForeignKey("filter.id", ondelete="CASCADE"))
    gearbox_id = Column(Integer, ForeignKey("gearbox.id", ondelete="CASCADE"))
    
    def __repr__(self):
        return f"GearboxFilter(id={self.id!r}, " \
               f"gearbox={self.gearbox.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
