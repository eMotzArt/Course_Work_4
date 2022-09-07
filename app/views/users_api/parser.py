from flask_restx import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, help='User name', nullable=False, required=True)
user_parser.add_argument('password', type=str, help='User password', nullable=False, required=True)
user_parser.add_argument('role', type=str, help='User role')

