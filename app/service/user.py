from app.dao import UserDAO
from app.utils import Security


class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def get_user(self):
        return self.dao.get_items()

    def get_user_by_pk(self, pk):
        return self.dao.get_item(pk)

    def add_new_user(self, **data):
        password = data.get('password')
        data['password'] = Security().get_hash(password)
        return self.dao.create_item(**data)

    def update_user_info(self, **kwargs):
        user = kwargs.get('user')
        new_data: dict = kwargs.get('parsed_data')
        for attribute, value in new_data.items():
            setattr(user, attribute, value)
        return
        # return self.dao.update_item(pk, **data)

    def update_user_password(self, **kwargs):
        old_password = kwargs.get('old_password')
        new_password = kwargs.get('new_password')
        user = kwargs.get('user')
        if Security().get_hash(old_password) == user.password:
            user.password = Security().get_hash(new_password)
        return

    def delete_user(self, pk):
        return self.dao.delete_item(pk)
