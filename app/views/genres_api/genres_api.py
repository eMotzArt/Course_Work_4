from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError

from app.service import GenreService
from .parser import genre_parser
api = Namespace('genres')

# api model
genre = api.model('Genre', {
    'id': fields.Integer(readonly=True, description='The genre unique identifier'),
    'name': fields.String(required=True, description='The genre name')
})

@api.route('/')
class GenresView(Resource):
    @api.marshal_list_with(genre)
    def get(self):
        return GenreService().get_genres()


@api.route('/<int:pk>/')
class GenreView(Resource):
    @api.response(code=404, description='Genre with this pk is not found in database')
    @api.marshal_with(genre)
    def get(self, pk):
        if result := GenreService().get_genre_by_pk(pk):
            return result, 200
        return '', 404

    @api.response(code=404, description='Genre with this pk is not found in database')
    @api.response(code=201, description='Successfully updated')
    @api.expect(genre_parser)
    @api.marshal_with(genre)
    # @auth_required(UserRole.admin, UserRole.uploader)
    def put(self, pk):
        data = genre_parser.parse_args()
        if result := GenreService().update_genre(pk, **data):
            return result, 201
        return '', 404

    @api.response(code=404, description='Director with this pk is not found in database')
    @api.response(code=204, description='Successfully updated')
    # @auth_required(UserRole.admin)
    def delete(self, pk):
        GenreService().delete_genre(pk)
        return '', 204

    @api.errorhandler(IntegrityError)
    def handle_exception(error):
        message = f"Error: {error.orig} with params: {error.params}"
        return {'message': message}, 500
