from .base import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .genre import Genre
from .user_favmovies import user_favmovies


class User(Base):
    __tablename__ = 'users'

    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(127))
    surname = Column(String(127))
    favorite_genre = Column(Integer, ForeignKey(Genre.id))
    genre = relationship(Genre)
    favorite_movies = relationship('Movie', secondary=user_favmovies)

