from .base import Base
from .genre import Genre
from .director import Director
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = 'movies'

    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    trailer = Column(String(100), nullable=False)
    #TODO добавить проверку на год
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre_id = Column(Integer, ForeignKey(Genre.id), nullable=False)
    genre = relationship('Genre')
    director_id = Column(Integer, ForeignKey(Director.id), nullable=False)
    director = relationship('Director')
