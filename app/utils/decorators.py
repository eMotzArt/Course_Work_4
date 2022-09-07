from flask import request, abort
from functools import wraps
from enum import Enum, unique

from .security import Security


@unique
class UserRole(Enum):
    admin = 'admin'
    uploader = 'uploader'
    user = 'user'


def auth_required(*roles):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                abort(401)

            auth_data = request.headers.get('Authorization')
            token = auth_data.split('Bearer ')[-1]
            if not Security().check_token(token):
                abort(401, 'Token invalid')

            user_info = Security().decode_token(token)
            role_text = user_info.get('role')
            try:
                role = UserRole(role_text)
            except ValueError:
                abort(401, 'Invalid token data')

            if role not in roles:
                abort(403)

            return func(*args, **kwargs)
        return wrapper
    return inner
