import pytest
from unittest.mock import MagicMock, patch

from app.dao import GenreDAO, DirectorDAO, MovieDAO
from app.dao.model import Genre, Director, Movie


@pytest.fixture()
@patch.object(GenreDAO, '__init__', lambda self: None)
def genre_dao():
    genre_dao = GenreDAO()
    genre_1 = Genre(id=1, name="Комедия")
    genre_2 = Genre(id=2, name="Ужасы")
    genre_3 = Genre(id=3, name="Боевик")
    genre_dao.get_item = MagicMock(return_value=genre_1)
    genre_dao.get_items = MagicMock(return_value=[genre_1, genre_2, genre_3])
    genre_dao.create_item = MagicMock(return_value=Genre(id=4, name="Мюзикл"))
    genre_dao.delete_item = MagicMock()
    genre_dao.update_item = MagicMock(return_value=genre_1)
    return genre_dao


@pytest.fixture()
@patch.object(DirectorDAO, '__init__', lambda self: None)
def director_dao():
    director_dao = DirectorDAO()
    director_1 = Director(id=1, name="Имя 1")
    director_2 = Director(id=2, name="Имя 2")
    director_3 = Director(id=3, name="Имя 3")
    director_dao.get_item = MagicMock(return_value=director_1)
    director_dao.get_items = MagicMock(return_value=[director_1, director_2, director_3])
    director_dao.create_item = MagicMock(return_value=Director(id=4, name="Имя 4"))
    director_dao.delete_item = MagicMock()
    director_dao.update_item = MagicMock(return_value=director_1)
    return director_dao

@pytest.fixture()
@patch.object(MovieDAO, '__init__', lambda self: None)
def movie_dao():
    movie_dao = MovieDAO()
    movie_1 = Movie(id=1, title="title_1", description='desc_1', trailer='youtube_1', year=1991, rating=6.6, genre_id=1, director_id=1)
    movie_2 = Movie(id=2, title="title_2", description='desc_2', trailer='youtube_2', year=1992, rating=7.7, genre_id=2, director_id=2)
    movie_3 = Movie(id=3, title="title_3", description='desc_3', trailer='youtube_3', year=1993, rating=8.8, genre_id=3, director_id=3)
    movie_dao.get_item = MagicMock(return_value=movie_1)
    movie_dao.get_items = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.create_item = MagicMock(return_value=Movie(id=4, title="title_4", description='desc_4', trailer='youtube_4', year=1994, rating=9.9, genre_id=4, director_id=4))
    movie_dao.delete_item = MagicMock()
    movie_dao.update_item = MagicMock(return_value=Movie(id=2, title='new_title', description='new_desc', trailer='new_tube', year=1990, rating=0.1, genre_id=5, director_id=5))
    movie_dao.add_movie_with_names = MagicMock(return_value=Movie(id=5, title="title_5", description='desc_5', trailer='youtube_5', year=1995, rating=10.0, genre_id=5, director_id=5))
    movie_dao.get_items_with_filtering = MagicMock(return_value=movie_3)
    return movie_dao