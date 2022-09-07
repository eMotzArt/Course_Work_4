from flask_restx import reqparse

auth_user_parser = reqparse.RequestParser()
auth_user_parser.add_argument('username', type=str, help='User name', nullable=False, required=True)
auth_user_parser.add_argument('password', type=str, help='User password', nullable=False, required=True)

auth_user_refresh_token_parser = reqparse.RequestParser()
auth_user_refresh_token_parser.add_argument('refresh_token', type=str, help='User refresh token', nullable=False, required=True)
