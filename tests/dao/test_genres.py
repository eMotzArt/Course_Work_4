import pytest

from typing import List
from unittest.mock import patch

from app.dao import GenreDAO
from app.dao.model import Genre


class TestGenreDAO:

    @pytest.fixture()
    @patch.object(GenreDAO, '__init__', lambda self: None)
    def genre_dao(self, db):
        genre_dao = GenreDAO()
        genre_dao.session = db.session
        return genre_dao

    @pytest.fixture
    def genre_1(self, db):
        g = Genre(name="Боевик")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def genre_2(self, db):
        g = Genre(name="Комедия")
        db.session.add(g)
        db.session.commit()
        return g
#get_items
    def test_get_items(self, genre_dao, genre_1, genre_2):
        result = genre_dao.get_items()
        assert len(result) == 2
        assert isinstance(result[0], Genre) and isinstance(result[1], Genre)
        assert isinstance(result, List)
        assert genre_1 in result
        assert genre_2 in result

    def test_get_items_pages(self, genre_dao, genre_2, genre_1):
        result = genre_dao.get_items(page=1)
        assert len(result) == 2
        assert isinstance(result, List)
        assert genre_1 in result
        assert genre_2 in result

        result = genre_dao.get_items(page=2)
        assert len(result) == 0
        assert isinstance(result, List)
#get_item
    def test_get_item(self, genre_dao, genre_2, genre_1):
        result = genre_dao.get_item(2)
        assert isinstance(result, Genre)
        assert result == genre_1

    def test_get_item_none(self, genre_dao, genre_2, genre_1):
        result = genre_dao.get_item(3)
        assert result == None
#create_item
    def test_get_create_item(self, db, genre_dao):
        assert len(genre_dao.get_items()) == 0
        new_item = genre_dao.create_item(name='test')
        db.session.commit()
        assert len(genre_dao.get_items()) == 1
        assert new_item.id == 1
        assert new_item.name == 'test'

    def test_get_create_item_error(self, db, genre_dao):
        with pytest.raises(TypeError):
            genre_dao.create_item(mistake='test')