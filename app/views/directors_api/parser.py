from flask_restx import reqparse

director_parser = reqparse.RequestParser()
director_parser.add_argument('name', type=str, help='Name of director', nullable=False, required=True)
