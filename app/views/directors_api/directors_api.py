from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError

from app.service import DirectorService
from .parser import director_parser
from app.utils.decorators import auth_required, UserRole


api = Namespace('directors')

# api model
director = api.model('Director', {
    'id': fields.Integer(readonly=True, description='Director unique identifier'),
    'name': fields.String(required=True, description='The director name')
})


@api.route('/')
class DirectorsView(Resource):
    @api.marshal_list_with(director)
    # @auth_required(UserRole.admin, UserRole.uploader, UserRole.user)
    def get(self):
        return DirectorService().get_directors(), 200

    @api.response(code=201, description="Successfully created")
    @api.response(code=500, description="Integrity Error")
    @api.expect(director_parser)
    @api.marshal_with(director)
    # @auth_required(UserRole.admin, UserRole.uploader)
    def post(self):
        data = director_parser.parse_args()
        return DirectorService().add_new_director(**data), 201


@api.route('/<int:pk>/')
class DirectorView(Resource):
    @api.marshal_with(director)
    @api.response(code=404, description='Director with this pk is not found in database')
    # @auth_required(UserRole.admin, UserRole.uploader, UserRole.user)
    def get(self, pk):
        if result := DirectorService().get_director_by_pk(pk):
            return result, 200
        return '', 404

    @api.response(code=404, description='Director with this pk is not found in database')
    @api.response(code=201, description='Successfully updated')
    @api.expect(director_parser)
    @api.marshal_with(director)
    # @auth_required(UserRole.admin, UserRole.uploader)
    def put(self, pk):
        data = director_parser.parse_args()
        if result := DirectorService().update_director(pk, **data):
            return result, 201
        return '', 404

    @api.response(code=204, description='Successfully deleted')
    @api.response(code=404, description='Director with this pk is not found in database')
    # @auth_required(UserRole.admin)
    def delete(self, pk):
        DirectorService().delete_director(pk)
        return '', 204

    @api.errorhandler(IntegrityError)
    def handle_exception(error):
        message = f"Error: {error.orig} with params: {error.params}"
        return {'message': message}, 500
