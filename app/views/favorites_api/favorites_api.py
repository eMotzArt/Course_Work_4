from flask_restx import Namespace, Resource

from app.utils import auth_required
from app.service import FavoriteService
from ..movies_api.movies_api import movie


api = Namespace('favorites')


@api.route('/movies/')
class FavView(Resource):
    @api.marshal_list_with(movie, code=200)
    @auth_required()
    def get(self, **kwargs):
        user = kwargs.get('user')
        return user.favorite_movies


@api.route('/movies/<int:pk>/')
class FavPKView(Resource):
    @auth_required()
    def post(self, pk, **kwargs):
        FavoriteService().append_movie_to_favorites(pk, **kwargs)
        return '', 204

    @auth_required()
    def delete(self, pk, **kwargs):
        FavoriteService().delete_movie_from_favorites(pk, **kwargs)
        return '', 204
