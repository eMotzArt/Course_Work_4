from app.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base

user_favmovies = Table(
    'users_favorite_movies',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id'))
)

