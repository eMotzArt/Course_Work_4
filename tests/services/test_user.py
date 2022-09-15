import pytest
from unittest.mock import patch

from app.dao.model import User
from app.service import UserService


class TestUserService:
    @pytest.fixture
    def user(self, db):
        g = User(email="user 1", password='password1')
        db.session.add(g)
        db.session.commit()
        return g

    @pytest.fixture()
    @patch('app.dao.UserDAO')
    def user_dao_mock(self, user_dao_mock):
        dao = user_dao_mock()
        return dao

    @pytest.fixture()
    @patch.object(UserService, '__init__', lambda self: None)
    def users_service(self, user_dao_mock):
        gs = UserService()
        gs.dao = user_dao_mock
        return gs

    def test_get_genres(self, users_service, user):
        data = {'name': 'test_name', 'surname': 'test_surname', 'favorite_genre': 5}
        users_service.update_user_info(user=user, parsed_data=data)

        assert user.name == data.get('name')
        assert user.surname == data.get('surname')
        assert user.favorite_genre == data.get('favorite_genre')

    @patch('app.utils.security.Security.get_hash',
           side_effect=['password1', 'new_password'])
    def test_update_user_password(self, get_hash, users_service, user):
        result = users_service.update_user_password(user=user, old_password='password1', new_password='no_mater_password_cause_mocked')
        assert result == True
        assert user.password == 'new_password'

    @patch('app.utils.security.Security.get_hash',
           side_effect=['wrong_password', 'new_password'])
    def test_update_user_password_wrong_password(self, get_hash, users_service, user):
        result = users_service.update_user_password(user=user, old_password='password1',
                                                    new_password='no_mater_password_cause_mocked')
        assert result == False
        assert user.password == 'password1'