import pytest

from typing import List
from unittest.mock import patch

from app.dao import UserDAO
from app.dao.model import User


class TestUserDAO:

    @pytest.fixture()
    @patch.object(UserDAO, '__init__', lambda self: None)
    def user_dao(self, db):
        user_dao = UserDAO()
        user_dao.session = db.session
        return user_dao

    @pytest.fixture
    def user_1(self, db):
        g = User(email="user 1", password='password1')
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def user_2(self, db):
        g = User(email="user 2", password='password2')
        db.session.add(g)
        db.session.commit()
        return g
#get_items
    def test_get_items(self, user_dao, user_1, user_2):
        result = user_dao.get_items()
        assert len(result) == 2
        assert isinstance(result[0], User) and isinstance(result[1], User)
        assert isinstance(result, List)
        assert user_1 in result
        assert user_2 in result

    def test_get_items_pages(self, user_dao, user_2, user_1):
        result = user_dao.get_items(page=1)
        assert len(result) == 2
        assert isinstance(result, List)
        assert user_1 in result
        assert user_2 in result

        result = user_dao.get_items(page=2)
        assert len(result) == 0
        assert isinstance(result, List)
#get_item
    def test_get_item(self, user_dao, user_2, user_1):
        result = user_dao.get_item(2)
        assert isinstance(result, User)
        assert result == user_1

    def test_get_item_none(self, user_dao, user_2, user_1):
        result = user_dao.get_item(3)
        assert result == None
#create_item
    def test_get_create_item(self, db, user_dao):
        assert len(user_dao.get_items()) == 0
        new_item = user_dao.create_item(email='user', password='password')
        db.session.commit()
        assert len(user_dao.get_items()) == 1
        assert new_item.id == 1
        assert new_item.email == 'user'
        assert new_item.password == 'password'

    def test_get_create_item_unknown_field(self, db, user_dao):
        with pytest.raises(TypeError):
            user_dao.create_item(email='user', password='password', mistake='mistake')