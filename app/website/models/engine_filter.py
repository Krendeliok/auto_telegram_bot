from models import Base
from sqlalchemy import Column, ForeignKey, Integer


class EngineFilter(Base):
    __tablename__ = 'engine_filter'
    id = Column(Integer, primary_key=True)
    filter_id = Column(Integer, ForeignKey("filter.id", ondelete="CASCADE"))
    engine_id = Column(Integer, ForeignKey("engine.id", ondelete="CASCADE"))
    
    def __repr__(self):
        return f"EngineFilter(id={self.id!r}, " \
               f"engine={self.engine.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
