from flask_restx import reqparse

genre_parser = reqparse.RequestParser()
genre_parser.add_argument('name', type=str, help='Name of genre', nullable=False, required=True)
