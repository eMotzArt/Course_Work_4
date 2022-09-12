from flask_restx import Namespace, Resource, fields

from .parser import auth_user_refresh_token_parser, auth_user_parser
from app.service import AuthService
from ..directors_api.directors_api import director
from ..genres_api.genres_api import genre
from ..movies_api.movies_api import movie
from app.utils import auth_required

api = Namespace('favorites')

user_favorite_movies = api.model('User_fav_movies', {
    'favorite_movies': fields.List(fields.Nested(movie))
})


@api.route('/movies/')
class FavView(Resource):
    @api.marshal_with(movie, code=200)
    @auth_required()
    def get(self, **kwargs):
        user = kwargs.get('user')
        return user.favorite_movies

@api.route('/movies/<int:pk>/')
class FavPKView(Resource):
    @auth_required()
    def post(self, pk, **kwargs):
        from app.dao import MovieDAO
        movie = MovieDAO().get_item(pk)
        from app.dao.model import User
        user: User = kwargs.get('user')
        user.favorite_movies.append(movie)
        return ''

    @auth_required()
    def delete(self, pk, **kwargs):
        from app.dao import MovieDAO
        movie = MovieDAO().get_item(pk)
        from app.dao.model import User
        user: User = kwargs.get('user')
        user.favorite_movies.remove(movie)
        return ''
        return
