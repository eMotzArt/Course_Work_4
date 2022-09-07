from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError

from app.views.users_api.parser import user_parser
from app.service import UserService


api = Namespace('users')

# api model
user = api.model('User', {
    'id': fields.Integer(readonly=True, description='User unique identifier'),
    'username': fields.String(required=True, description='User name'),
    'password': fields.String(required=True, description='User password'),
    'role': fields.String(required=True, description='User role')
})

@api.route('/')
class UsersView(Resource):
    @api.marshal_list_with(user)
    def get(self):
        return UserService().get_users()

    @api.expect(user_parser)
    @api.marshal_with(user, code=201)
    def post(self):
        data = user_parser.parse_args()
        return UserService().add_new_user(**data)

@api.route('/<int:pk>/')
class UserView(Resource):
    @api.marshal_with(user)
    @api.response(code=404, description='User with this pk is not found in database')
    def get(self, pk):
        if result := UserService().get_user_by_pk(pk):
            return result, 200
        return '', 404

    @api.expect(user_parser)
    @api.response(code=204, description="Successfully modified")
    @api.marshal_with(user)
    def put(self, pk):
        data = user_parser.parse_args()
        return UserService().update_user(pk, **data)

    @api.response(code=204, description="Successfully deleted")
    def delete(self, pk):
        UserService().delete_user(pk)
        return None, 204

    @api.errorhandler(IntegrityError)
    def handle_exception(error):
        message = f"Error: {error.orig} with params: {error.params}"
        return {'message': message}, 500