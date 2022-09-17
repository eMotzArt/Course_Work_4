from sqlalchemy import Column, ForeignKey, Table

from .base import Base

user_favmovies = Table(
    'users_favorite_movies',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id'))
)
