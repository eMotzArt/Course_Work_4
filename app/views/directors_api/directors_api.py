from flask_restx import Namespace, Resource, fields

from app.service import DirectorService

from .parser import director_query_parser


api = Namespace('directors')


# api model
director = api.model('Director', {
    'id': fields.Integer(readonly=True, description='Director unique identifier'),
    'name': fields.String(required=True, description='The director name')
})


@api.route('/')
class DirectorsView(Resource):
    @api.marshal_list_with(director)
    @api.expect(director_query_parser)
    def get(self):
        params = director_query_parser.parse_args()
        return DirectorService().get_directors(**params), 200


@api.route('/<int:pk>/')
class DirectorView(Resource):
    @api.marshal_with(director)
    @api.response(code=404, description='Director with this pk is not found in database')
    def get(self, pk):
        if result := DirectorService().get_director_by_pk(pk):
            return result, 200
        return '', 404
