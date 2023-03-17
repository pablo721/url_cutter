from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import DB_CONN_STRING



engine = create_engine(DB_CONN_STRING, connect_args={'check_same_thread': False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


