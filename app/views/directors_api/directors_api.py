from flask_restx import Namespace, Resource, fields

from app.service import DirectorService


api = Namespace('directors')


# api model
director = api.model('Director', {
    'id': fields.Integer(readonly=True, description='Director unique identifier'),
    'name': fields.String(required=True, description='The director name')
})


@api.route('/')
class DirectorsView(Resource):
    @api.marshal_list_with(director)
    def get(self):
        return DirectorService().get_directors(), 200


@api.route('/<int:pk>/')
class DirectorView(Resource):
    @api.marshal_with(director)
    @api.response(code=404, description='Director with this pk is not found in database')
    def get(self, pk):
        if result := DirectorService().get_director_by_pk(pk):
            return result, 200
        return '', 404
