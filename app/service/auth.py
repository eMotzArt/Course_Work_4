from flask import abort

from app.dao import AuthDAO
from app.utils import Security


class AuthService:
    def __init__(self):
        self.dao = AuthDAO()

    def get_tokens_by_login_password(self, **data):
        user_name = data.get('username', None)
        user_password = data.pop('password', None)

        if None in [user_name, user_password]:
            abort(400)

        if not (user := self.dao.get_user_by_name(user_name)):
            abort(404)

        if not Security.is_passwords_equals(Security().get_hash(user_password), user.password):
            abort(401)

        data['role'] = str(user.role)
        data['user_id'] = user.id
        tokens = Security().generate_tokens(**data)
        self.dao.record_refresh_token(user.id, tokens['refresh_token'])
        return tokens

    def get_tokens_by_refresh_token(self, **data):
        refresh_token = data.pop('refresh_token')
        user_info = Security().decode_token(refresh_token)
        user_id = user_info.get('user_id')

        if not self.dao.compare_refresh_tokens(user_id, refresh_token):
            abort(401)

        user_info.pop('exp')
        tokens = Security().generate_tokens(**user_info)
        self.dao.record_refresh_token(user_id, tokens['refresh_token'])
        return tokens
