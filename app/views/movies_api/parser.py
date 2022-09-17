from flask_restx import reqparse


movie_query_parser = reqparse.RequestParser()
movie_query_parser.add_argument('status', type=str, help='new movie filtering parrameter', store_missing=False)
movie_query_parser.add_argument('page', type=int, help='pagination by 12 items', store_missing=False)
