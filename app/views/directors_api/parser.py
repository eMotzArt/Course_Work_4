from flask_restx import reqparse


director_query_parser = reqparse.RequestParser()
director_query_parser.add_argument('page', type=int, help='pagination by 12 items', store_missing=False)
