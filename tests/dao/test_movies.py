import pytest

from typing import List
from unittest.mock import patch

from app.dao import MovieDAO
from app.dao.model import Movie


class TestMovieDAO:

    @pytest.fixture()
    @patch.object(MovieDAO, '__init__', lambda self: None)
    def movie_dao(self, db):
        movie_dao = MovieDAO()
        movie_dao.session = db.session
        return movie_dao

    @pytest.fixture
    def movie_1(self, db):
        g = Movie(title="Movie 1 title",
                  description='Movie 1 description',
                  trailer='Movie 1 trailer link',
                  year=2021,
                  rating=8.8,
                  genre_id=1,
                  director_id=1,
                  )
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def movie_2(self, db):
        g = Movie(title="Movie 2 title",
                  description='Movie 2 description',
                  trailer='Movie 2 trailer link',
                  year=2022,
                  rating=9.9,
                  genre_id=2,
                  director_id=2
                  )
        db.session.add(g)
        db.session.commit()
        return g
# get_items

    def test_get_items(self, movie_dao, movie_1, movie_2):
        result = movie_dao.get_items()
        assert len(result) == 2
        assert isinstance(result[0], Movie) and isinstance(result[1], Movie)
        assert isinstance(result, List)
        assert movie_1 in result
        assert movie_2 in result

    def test_get_items_status(self, movie_dao, movie_1, movie_2):
        result = movie_dao.get_items(status='new')
        assert result[0] == movie_2 and result[1] == movie_1

        result = movie_dao.get_items(page=2)
        assert len(result) == 0
        assert isinstance(result, List)

    def test_get_items_pages(self, movie_dao, movie_2, movie_1):
        result = movie_dao.get_items(page=1)
        assert len(result) == 2
        assert isinstance(result, List)
        assert movie_1 in result
        assert movie_2 in result

        result = movie_dao.get_items(page=2)
        assert len(result) == 0
        assert isinstance(result, List)
# get_item

    def test_get_item(self, movie_dao, movie_2, movie_1):
        result = movie_dao.get_item(2)
        assert isinstance(result, Movie)
        assert result == movie_1

    def test_get_item_none(self, movie_dao, movie_2, movie_1):
        result = movie_dao.get_item(3)
        assert result == None
#create_item
    def test_get_create_item(self, db, movie_dao):
        assert len(movie_dao.get_items()) == 0
        data = {
            'title': "Movie 1 title",
            'description': 'Movie 1 description',
            'trailer': 'Movie 1 trailer link',
            'year': 2021,
            'rating': 8.8,
            'genre_id': 1,
            'director_id': 1
        }
        new_item = movie_dao.create_item(**data)
        db.session.commit()
        assert len(movie_dao.get_items()) == 1
        assert new_item.id == 1
        for k, v in data.items():
            assert getattr(new_item, k) == v

    def test_get_create_item_error(self, db, movie_dao):
        with pytest.raises(TypeError):
            movie_dao.create_item(mistake='test')
