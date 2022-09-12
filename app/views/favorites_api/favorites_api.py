from flask_restx import Namespace, Resource, fields

from app.utils import auth_required
from app.dao import MovieDAO
from app.dao.model import User
from ..movies_api.movies_api import movie


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
        selected_movie = MovieDAO().get_item(pk)
        user: User = kwargs.get('user')
        user.favorite_movies.append(selected_movie)
        return '', 204

    @auth_required()
    def delete(self, pk, **kwargs):
        movie = MovieDAO().get_item(pk)
        user: User = kwargs.get('user')
        user.favorite_movies.remove(movie)
        return '', 204
