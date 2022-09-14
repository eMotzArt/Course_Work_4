from flask_restx import Namespace, Resource, fields

from app.service import MovieService
from .parser import movie_query_parser
from ..genres_api.genres_api import genre
from ..directors_api.directors_api import director

api = Namespace('movies')

# api model
movie = api.model('Movie', {
    'id': fields.Integer(readonly=True, description='Movie unique identifier'),
    'title': fields.String(required=True, description='Movie title'),
    'description': fields.String(required=True, description='Movie description'),
    'trailer': fields.String(required=False, description='Movie trailer link'),
    'year': fields.Integer(required=True, description='Movie release year'),
    'rating': fields.Float(required=False, description='Movie rating'),
    'genre_id': fields.Integer(required=True, description='Genre id'),
    'genre': fields.Nested(genre),
    'director_id': fields.Integer(required=True, description='Director id'),
    'director': fields.Nested(director)
})


@api.route('/')
class MoviesView(Resource):
    @api.expect(movie_query_parser)
    @api.marshal_list_with(movie)
    def get(self):
        params = movie_query_parser.parse_args()
        return MovieService().get_movies(**params), 200


@api.route('/<int:pk>/')
class MovieView(Resource):
    @api.marshal_with(movie)
    @api.response(code=404, description='Item not found')
    def get(self, pk):
        if result := MovieService().get_movie_by_pk(pk):
            return result, 200
        return '', 404
