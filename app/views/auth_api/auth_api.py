from flask_restx import Namespace, Resource, fields

from .parser import auth_user_parser, auth_user_refresh_token_parser
from app.service import AuthService


api = Namespace('auth')

# api model
user_tokens = api.model('User_token', {
    'access_token': fields.String(required=True, description='User access token'),
    'refresh_token': fields.String(required=True, description='User refresh token')
})

@api.route('/')
class AuthView(Resource):
    @api.expect(auth_user_parser)
    @api.marshal_with(user_tokens, code=201)
    def post(self):
        data = auth_user_parser.parse_args()
        return AuthService().get_tokens_by_login_password(**data), 201

    @api.expect(auth_user_refresh_token_parser)
    @api.marshal_with(user_tokens, code=201)
    def put(self):
        data = auth_user_refresh_token_parser.parse_args()
        return AuthService().get_tokens_by_refresh_token(**data)
