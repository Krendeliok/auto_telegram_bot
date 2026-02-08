from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
)
from models import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    advertisement_id = Column(Integer, ForeignKey("adv.id", ondelete="CASCADE"))
    source = Column(String, nullable=False)
    cloudinary_source = Column(String, nullable=False)


    def __repr__(self):
        return f"Image(id={self.id!r}, " \
               f"advertisement={self.advertisement.id!r}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
