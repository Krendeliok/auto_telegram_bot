from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Date,
    Boolean
)
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship
from datetime import date
from dateutil.relativedelta import relativedelta
from models import Base


expires_at = {
    "months": 1
}

class AditionalAdvertisements(Base):
    __tablename__ = 'additional_advs'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.id", ondelete="CASCADE"))
    start = Column(Date)
    end = Column(Date)
    reserved = Column(Boolean, default=expression.false(), server_default=expression.false(), nullable=False)

    advertisement = relationship(
        "Advertisement",
        backref="additional_adv",
        uselist=False
    )

    def update_expires_dates(self):
        if not self.reserved:
            self.reserved = expression.true()
            self.start = date.today()
            self.end = date.today()

        self.end = self.end + relativedelta(**expires_at)

    def __repr__(self):
        return f"Country(id={self.id!r}, " \
               f"name={self.name!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
