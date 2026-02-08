from models import Base
from sqlalchemy import Column, ForeignKey, Integer


class ModelFilter(Base):
    __tablename__ = 'model_filter'
    id = Column(Integer, primary_key=True)
    producer_filter_id = Column(Integer, ForeignKey("producer_filter.id", ondelete="CASCADE"))
    model_id = Column(Integer, ForeignKey("model.id", ondelete="CASCADE"))
    
    def __repr__(self):
        return f"ModelFilter(id={self.id!r}, " \
               f"model={self.model.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
