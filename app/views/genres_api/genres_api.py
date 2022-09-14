from flask_restx import Namespace, Resource, fields

from app.service import GenreService

from .parser import genre_query_parser


api = Namespace('genres')


# api model
genre = api.model('Genre', {
    'id': fields.Integer(readonly=True, description='The genre unique identifier'),
    'name': fields.String(required=True, description='The genre name')
})


@api.route('/')
class GenresView(Resource):
    @api.expect(genre_query_parser)
    @api.marshal_list_with(genre)
    def get(self):
        params = genre_query_parser.parse_args()
        return GenreService().get_genres(**params)


@api.route('/<int:pk>/')
class GenreView(Resource):
    @api.response(code=404, description='Genre with this pk is not found in database')
    @api.marshal_with(genre)
    def get(self, pk):
        if result := GenreService().get_genre_by_pk(pk):
            return result, 200
        return '', 404

