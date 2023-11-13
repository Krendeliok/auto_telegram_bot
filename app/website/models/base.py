from sqlalchemy.orm import declarative_base


Base = declarative_base()
Base.__mapper_args__ = {
    'confirm_deleted_rows': False
}
