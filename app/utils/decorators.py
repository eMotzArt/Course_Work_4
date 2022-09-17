from flask import request, abort
from functools import wraps

from .security import Security
from app.dao import UserDAO

def auth_required(*roles):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                print('ОТСУТСТВУЕТ ЗАГОЛОВОК АВТОРИЗАЦИИ')
                abort(401)
            auth_data = request.headers.get('Authorization')
            token = auth_data.split('Bearer ')[-1]
            print(f'ПОПЫТКА ДОСТУПА ПО ТОКЕНУ: {token}')
            if not Security().check_token(token):
                print('ACCESS TOKEN НЕ ВАЛИДЕН')
                abort(401)
            print('TOKEN ВЕРЕН!!!')
            user_info = Security().decode_token(token)
            user_id = user_info.get('user_id')
            user = UserDAO().get_item(user_id)
            kwargs['user'] = user
            return func(*args, **kwargs)
        return wrapper
    return inner
