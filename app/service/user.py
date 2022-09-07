from app.dao import UserDAO
from app.utils import Security


class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def get_users(self):
        return self.dao.get_items()

    def get_user_by_pk(self, pk):
        return self.dao.get_item(pk)

    def add_new_user(self, **data):
        password = data.get('password')
        data['password'] = Security().get_hash(password)
        return self.dao.create_item(**data)

    def update_user(self, pk, **data):
        return self.dao.update_item(pk, **data)

    def delete_user(self, pk):
        return self.dao.delete_item(pk)
