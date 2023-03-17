from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, Column, ForeignKey, Integer, DateTime
from .db import Base



class Link(Base):
    __tablename__ = 'link'
    url = Column(String(length=2048), nullable=False)
    expire_date = Column(DateTime, nullable=True)
    short_url_suffix = Column(String(length=16), nullable=False, primary_key=True)



