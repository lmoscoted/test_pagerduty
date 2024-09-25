from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy 

from config import Config


db = SQLAlchemy()


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

metadata = MetaData()

Base = declarative_base(metadata=metadata)

# Create a sessionmaker to create db sessions
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


# Listen for events to control session behavior
@event.listens_for(SessionLocal, "after_begin")
def receive_after_begin(session, *args, **kwargs):
    session.expire_on_commit = False

@event.listens_for(SessionLocal, "after_flush")
def receive_after_flush(session,  *args, **kwargs):
    session.expire_on_commit = True