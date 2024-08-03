from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from models import Base
from config import DATABASE_URI


engine = create_engine(DATABASE_URI)
Base.metadata.bind = engine

session = Session(engine)
