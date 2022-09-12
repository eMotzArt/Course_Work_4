from flask_restx import Namespace, Resource, fields

from .parser import user_update_info_parser, user_update_password_parser
from app.service import UserService
from app.utils import auth_required


api = Namespace('user')


# api model
user = api.model('User', {
    'name': fields.String(required=True, description='User name'),
    'surname': fields.String(required=True, description='User password'),
    'favorite_genre': fields.Integer(required=True, description='User role'),
    # для костыля, описал ниже
    'favourite_genre': fields.Integer(required=True, description='fix')
})

@api.route('/')
class UserView(Resource):
    @api.marshal_list_with(user)
    @auth_required()
    def get(self, **kwargs):
        user = kwargs.get('user')
        # Эта строчка - костыль, т.к. в front-end'e ожидается  не favorite_genre, а  favourite_genre
        user.favourite_genre = user.favorite_genre
        return user, 200

    @api.expect(user_update_info_parser)
    @auth_required()
    def patch(self, **kwargs):
        new_data = user_update_info_parser.parse_args()
        #  Эта строчка - костыль, т.к. с фронта приходит не favorite_genre, а favourite_genre
        if wrong_genre := new_data.pop('favourite_genre'):
            new_data['favorite_genre'] = wrong_genre
        kwargs['parsed_data'] = new_data
        UserService().update_user_info(**kwargs)
        return '', 204

@api.route('/password/')
class UserPassView(Resource):
    @api.expect(user_update_password_parser)
    @auth_required()
    def put(self, **kwargs):
        passwords = user_update_password_parser.parse_args()
        UserService().update_user_password(**kwargs, **passwords)
        return '', 204
