from sqlalchemy import Column, String
from .base import Base

class Genre(Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)
