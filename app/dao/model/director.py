from sqlalchemy import Column, String
from .base import Base

class Director(Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)
