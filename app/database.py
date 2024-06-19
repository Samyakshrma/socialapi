from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY = 'postgresql://postgres:hellothere@localhost/social'

engine = create_engine(SQL_ALCHEMY)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()
