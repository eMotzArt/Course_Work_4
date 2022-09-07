from flask import g

from app.database import db
from app.dao.model import Movie, Genre, Director, User, UserToken


class BaseDAO():
    def __init__(self):
        self.session = g.session
        self.model: db.Model

    def get_items(self):
        return self.model.query.all()

    def get_item(self, pk):
        return self.model.query.get(pk)

    def create_item(self, **data):
        new_item = self.model(**data)
        self.session.add(new_item)
        self.session.flush()
        return new_item

    def update_item(self, pk, **data):
        self.model.query.filter_by(id=pk).update(data)
        return self.model.query.filter_by(id=pk).first()

    def delete_item(self, pk):
        self.model.query.filter_by(id=pk).delete()


class MovieDAO(BaseDAO):
    model = Movie

    def get_or_create_parent_id(self, query, model):
        item = self.session.query(model).filter(model.name.ilike(query)).first()
        if not item:
            item = model(name=query)
            self.session.add(item)
            self.session.flush()
        return item.id

    def add_movie_with_names(self, **data):
        director_name = data.pop('director_name')
        genre_name = data.pop('genre_name')
        if director_name:
            director_id = self.get_or_create_parent_id(director_name, Director)
        if genre_name:
            genre_id = self.get_or_create_parent_id(genre_name, Genre)
        data.update({'director_id': director_id, 'genre_id': genre_id})
        return super().create_item(**data)

    def get_items_with_filtering(self, **params):
        query = self.model.query
        for filter_ in params:
            if value := params.get(filter_):
                query = query.filter(getattr(self.model, filter_) == value)
        return query.all()


class GenreDAO(BaseDAO):
    model = Genre


class DirectorDAO(BaseDAO):
    model = Director


class UserDAO(BaseDAO):
    model = User


class AuthDAO(BaseDAO):
    model = User

    def get_user_by_name(self, username):
        if user := self.model.query.filter_by(username=username).first():
            return user

    def record_refresh_token(self, user_id, token):
        if user := self.session.query(UserToken).filter_by(user_id=user_id).first():
            user.refresh_token = token
        else:
            user_token = UserToken(user_id=user_id, refresh_token=token)
            self.session.add(user_token)
        self.session.flush()

    def compare_refresh_tokens(self, user_id, user_refresh_token):
        if user := self.session.query(UserToken).filter_by(user_id=user_id).first():
            if user.refresh_token == user_refresh_token:
                return True
        return False
