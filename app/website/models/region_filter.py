from models import Base
from sqlalchemy import Column, ForeignKey, Integer


class RegionFilter(Base):
    __tablename__ = 'region_filter'
    id = Column(Integer, primary_key=True)
    filter_id = Column(Integer, ForeignKey("filter.id", ondelete="CASCADE"))
    region_id = Column(Integer, ForeignKey("country.id", ondelete="CASCADE"))
    
    def __repr__(self):
        return f"RegionFilter(id={self.id!r}, " \
               f"region={self.region.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
