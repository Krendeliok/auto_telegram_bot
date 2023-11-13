from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
)
from sqlalchemy.sql import expression
from models import Base

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    advertisement_id = Column(Integer, ForeignKey("adv.id", ondelete="CASCADE"), nullable=True)
    verified = Column(Boolean, default=expression.false(), server_default=expression.false(), nullable=False)

    def __repr__(self):
        return f"Feedback(id={self.id!r}, " \
               f"name={self.name!r}, " \
               f"phone={self.phone!r}," \
               f"verified={self.verified!r})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
