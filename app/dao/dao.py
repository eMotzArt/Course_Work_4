from flask import g
from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from app.database import db
from .model import Movie, Genre, Director, User, UserToken


class BaseDAO():
    def __init__(self):
        self.session = g.session
        self.model: db.Model

    def get_items(self, **params):
        query = self.model.query
        if params.get('status'):
            query = query.order_by(desc(self.model.year)).order_by(desc(self.model.created))
        if page := params.get('page'):
            try:
                return query.paginate(page, 12).items
            except NotFound:
                return []
        return query.all()

    def get_item(self, pk):
        return self.model.query.get(pk)

    def create_item(self, **data):
        new_item = self.model(**data)
        self.session.add(new_item)
        return new_item


class MovieDAO(BaseDAO):
    model = Movie


class GenreDAO(BaseDAO):
    model = Genre


class DirectorDAO(BaseDAO):
    model = Director


class UserDAO(BaseDAO):
    model = User


class AuthDAO(BaseDAO):
    model = User

    def get_user_by_name(self, email):
        if user := self.model.query.filter_by(email=email).first():
            return user

    def record_refresh_token(self, user_id, token):
        if user := self.session.query(UserToken).filter_by(user_id=user_id).first():
            user.refresh_token = token
        else:
            user_token = UserToken(user_id=user_id, refresh_token=token)
            self.session.add(user_token)

    def compare_refresh_tokens(self, user_id, user_refresh_token):
        if user := self.session.query(UserToken).filter_by(user_id=user_id).first():
            if user.refresh_token == user_refresh_token:
                return True
        return False
