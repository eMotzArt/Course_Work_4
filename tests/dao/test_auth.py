import pytest

from typing import List
from unittest.mock import patch

from app.dao import AuthDAO
from app.dao.model import User, UserToken


class TestAuthDAO:

    @pytest.fixture()
    @patch.object(AuthDAO, '__init__', lambda self: None)
    def auth_dao(self, db):
        auth_dao = AuthDAO()
        auth_dao.session = db.session
        return auth_dao

    @pytest.fixture
    def user_1(self, db):
        g = User(email="user1@test.com", password='password1')
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def user_2(self, db):
        g = User(email="user2@test.com", password='password2')
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture
    def usertoken_1(self, db):
        g = UserToken(user_id=1, refresh_token='testtoken')
        db.session.add(g)
        db.session.commit()
        return g


#get_items
    def test_get_items(self, auth_dao, user_1, user_2):
        result = auth_dao.get_items()
        assert len(result) == 2
        assert isinstance(result[0], User) and isinstance(result[1], User)
        assert isinstance(result, List)
        assert user_1 in result
        assert user_2 in result

    def test_get_items_pages(self, auth_dao, user_2, user_1):
        result = auth_dao.get_items(page=1)
        assert len(result) == 2
        assert isinstance(result, List)
        assert user_1 in result
        assert user_2 in result

        result = auth_dao.get_items(page=2)
        assert len(result) == 0
        assert isinstance(result, List)
#get_item
    def test_get_item(self, auth_dao, user_2, user_1):
        result = auth_dao.get_item(2)
        assert isinstance(result, User)
        assert result == user_1

    def test_get_item_none(self, auth_dao, user_2, user_1):
        result = auth_dao.get_item(3)
        assert result == None
#create_item
    def test_get_create_item(self, db, auth_dao):
        assert len(auth_dao.get_items()) == 0
        new_item = auth_dao.create_item(email='user', password='password')
        db.session.commit()
        assert len(auth_dao.get_items()) == 1
        assert new_item.id == 1
        assert new_item.email == 'user'
        assert new_item.password == 'password'

    def test_get_create_item_unknown_field(self, db, auth_dao):
        with pytest.raises(TypeError):
            auth_dao.create_item(email='user', password='password', mistake='mistake')
#get_user_by_name
    def test_get_user_by_name(self, auth_dao, user_1, user_2):
        result = auth_dao.get_user_by_name('user2@test.com')
        assert isinstance(result, User)
        assert result == user_2

    def test_get_user_by_name_none(self, auth_dao, user_1, user_2):
        result = auth_dao.get_user_by_name('user3@test.com')
        assert result == None
#record_refresh_token
    def test_record_refresh_token(self, auth_dao, user_1, usertoken_1):
        auth_dao.record_refresh_token(1, 'new_token')
        token = UserToken.query.first()
        assert token.refresh_token == 'new_token'
        assert token.user_for_token == user_1

    def test_record_refresh_token_new_user(self, auth_dao, user_1):
        auth_dao.record_refresh_token(1, 'token')
        token = UserToken.query.first()
        assert token.refresh_token == 'token'
        assert token.user_for_token == user_1
#compare_refresh_tokens
    def test_compare_refresh_tokens_true(self, auth_dao, user_1, usertoken_1):
        result = auth_dao.compare_refresh_tokens(1,'testtoken')
        assert result == True

    def test_compare_refresh_tokens_false(self, auth_dao, user_1, usertoken_1):
        result = auth_dao.compare_refresh_tokens(1,'wrong_token')
        assert result == False

