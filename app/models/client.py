from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    BigInteger,
)
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship
from models import Base, Advertisement


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False)
    phone_number = Column(String, nullable=False)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_vip = Column(Boolean, default=expression.false(), server_default=expression.false(), nullable=False)
    is_admin = Column(Boolean, default=expression.false(), server_default=expression.false(), nullable=False)
    is_owner = Column(Boolean, default=expression.false(), server_default=expression.false(), nullable=False)

    advertisements = relationship(
        "Advertisement",
        foreign_keys=[Advertisement.user_id],
        backref="client"
    )

    filters = relationship(
        "Filter",
        backref="client"
    )

    def __repr__(self):
        return f"Client(id={self.id!r}, " \
               f"first_name={self.first_name!r}, " \
               f"last_name={self.last_name!r}, " \
               f"username={self.username!r})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
