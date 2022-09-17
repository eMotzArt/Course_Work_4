from flask_restx import reqparse

user_update_info_parser = reqparse.RequestParser()
user_update_info_parser.add_argument('name', type=str, help='User name')#, nullable=False, required=True)
user_update_info_parser.add_argument('surname', type=str, help='User surname')#, nullable=False, required=True)
user_update_info_parser.add_argument('favourite_genre', type=int, help='User favorite genre id')

user_update_password_parser = reqparse.RequestParser()
user_update_password_parser.add_argument('old_password', type=str, help='User current password', nullable=False, required=True)
user_update_password_parser.add_argument('new_password', type=str, help='User new password', nullable=False, required=True)
