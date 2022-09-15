import pytest

from typing import List
from unittest.mock import patch

from app.dao import DirectorDAO
from app.dao.model import Director


class TestDirectorDAO:

    @pytest.fixture()
    @patch.object(DirectorDAO, '__init__', lambda self: None)
    def director_dao(self, db):
        director_dao = DirectorDAO()
        director_dao.session = db.session
        return director_dao

    @pytest.fixture
    def director_1(self, db):
        g = Director(name="Боевик")
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def director_2(self, db):
        g = Director(name="Комедия")
        db.session.add(g)
        db.session.commit()
        return g
#get_items
    def test_get_items(self, director_dao, director_1, director_2):
        result = director_dao.get_items()
        assert len(result) == 2
        assert isinstance(result[0], Director) and isinstance(result[1], Director)
        assert isinstance(result, List)
        assert director_1 in result
        assert director_2 in result

    def test_get_items_pages(self, director_dao, director_2, director_1):
        result = director_dao.get_items(page=1)
        assert len(result) == 2
        assert isinstance(result, List)
        assert director_1 in result
        assert director_2 in result

        result = director_dao.get_items(page=2)
        assert len(result) == 0
        assert isinstance(result, List)
#get_item
    def test_get_item(self, director_dao, director_2, director_1):
        result = director_dao.get_item(2)
        assert isinstance(result, Director)
        assert result == director_1

    def test_get_item_none(self, director_dao, director_2, director_1):
        result = director_dao.get_item(3)
        assert result == None
#create_item
    def test_get_create_item(self, db, director_dao):
        assert len(director_dao.get_items()) == 0
        new_item = director_dao.create_item(name='test')
        db.session.commit()
        assert len(director_dao.get_items()) == 1
        assert new_item.id == 1
        assert new_item.name == 'test'

    def test_get_create_item_error(self, db, director_dao):
        with pytest.raises(TypeError):
            director_dao.create_item(mistake='test')