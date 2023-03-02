from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Date,
    Boolean,
    Float,
)
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship
from models import Base


class AditionalSearch(Base):
    __tablename__ = 'search'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"))
    start = Column(Date)
    end = Column(Date)
    reserved = Column(Boolean, default=expression.false(), server_default=expression.false(), nullable=False)
    producer_id = Column(Integer, ForeignKey("producer.id", ondelete="SET NULL"))
    model_id = Column(Integer, ForeignKey("model.id", ondelete="SET NULL"))
    
    min_price = Column(Integer, default=0, server_default='0', nullable=False)
    max_price = Column(Integer, default=0, server_default='0', nullable=False)
    min_year = Column(Integer, default=0, server_default='0', nullable=False)
    max_year = Column(Integer, default=0, server_default='0', nullable=False)
    min_engine_volume = Column(Float, default=0, server_default='0', nullable=False)
    max_engine_volume = Column(Float, default=0, server_default='0', nullable=False)
    min_range = Column(Integer, default=0, server_default='0', nullable=False)
    max_range = Column(Integer, default=0, server_default='0', nullable=False)

    def __repr__(self):
        return f"Country(id={self.id!r}, " \
               f"name={self.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
