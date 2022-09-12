from flask_restx import Namespace, Resource, fields

from app.service import GenreService


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

