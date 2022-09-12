from .base import Base
from .genre import Genre
from .director import Director
from sqlalchemy import Column, String, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = 'movies'

    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    trailer = Column(String(100), nullable=False)
    year = Column(Integer, CheckConstraint('year >= 0'), nullable=False)
    rating = Column(Float, CheckConstraint('rating >= 0.0 and rating <= 10.0'), nullable=False)
    genre_id = Column(Integer, ForeignKey(Genre.id), nullable=False)
    genre = relationship(Genre)
    director_id = Column(Integer, ForeignKey(Director.id), nullable=False)
    director = relationship(Director)
