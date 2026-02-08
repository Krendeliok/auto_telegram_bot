from models import Base
from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression


class ProducerFilter(Base):
    __tablename__ = 'producer_filter'
    id = Column(Integer, primary_key=True)
    filter_id = Column(Integer, ForeignKey("filter.id", ondelete="CASCADE"))
    producer_id = Column(Integer, ForeignKey("producer.id", ondelete="CASCADE"))
    all_models = Column(Boolean, default=expression.true(), server_default=expression.true())
    

    models_filter = relationship(
        "ModelFilter",
        backref="producer_filter"
    )

    def __repr__(self):
        return f"ProducerFilter(id={self.id!r}, " \
               f"producer={self.producer.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
