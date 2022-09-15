import pytest
from unittest.mock import patch
from werkzeug.exceptions import BadRequest, Unauthorized

from app.service import AuthService



class TestUserService:
    @pytest.fixture()
    @patch('app.dao.AuthDAO')
    def auth_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.record_refresh_token.return_value = True
        dao.compare_refresh_tokens.return_value = True
        dao.create_item.return_value = True
        return dao

    @pytest.fixture()
    @patch.object(AuthService, '__init__', lambda self: None)
    def auth_service(self, auth_dao_mock):
        auth_service = AuthService()
        auth_service.dao = auth_dao_mock
        return auth_service


    @patch('app.utils.security.Security.generate_tokens', return_value={'access_token': 1, 'refresh_token': 2})
    @patch('app.utils.security.Security.is_passwords_equals', return_value=True)
    def test_get_tokens_by_login_password(self, sec_equals_pass, sec_generate_token, auth_service):
        result = auth_service.get_tokens_by_login_password(email='a@b.c', password='password')
        assert result == {'access_token': 1, 'refresh_token': 2}

    @patch('app.utils.security.Security.generate_tokens', return_value={'access_token': 1, 'refresh_token': 2})
    @patch('app.utils.security.Security.is_passwords_equals', return_value=True)
    def test_get_tokens_by_login_password_no_entry_data(self, sec_equals_pass, sec_generate_token, auth_service):
        with pytest.raises(BadRequest):
            auth_service.get_tokens_by_login_password(password='password')

    @patch('app.utils.security.Security.generate_tokens', return_value={'access_token': 1, 'refresh_token': 2})
    @patch('app.utils.security.Security.is_passwords_equals', return_value=False)
    def test_get_tokens_by_login_password_wrong_password(self, sec_equals_pass, sec_generate_token, auth_service):
        with pytest.raises(Unauthorized):
            auth_service.get_tokens_by_login_password(email='a@b.c', password='password')

    @patch('app.utils.security.Security.decode_token', return_value={'user_id': 'id', 'exp': 'exp'})
    @patch('app.utils.security.Security.generate_tokens', return_value={'access_token': 1, 'refresh_token': 2})
    @patch('app.utils.security.Security.is_passwords_equals', return_value=True)
    def test_get_tokens_by_refresh_token(self, sec_equals_pass, sec_generate_token, decode_token, auth_service):
        result = auth_service.get_tokens_by_refresh_token(refresh_token='token')
        assert result == {'access_token': 1, 'refresh_token': 2}

    @patch('app.utils.security.Security.get_hash', return_value=True)
    def test_register_new_user(self, decode_token, auth_service):
        result = auth_service.register_new_user(password='test')
        assert result == True
