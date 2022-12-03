from sqlalchemy.orm import Session

session: Session = None

def create_session(engine):
    global session
    session = Session(engine)
    return session