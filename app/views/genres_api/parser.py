from flask_restx import reqparse


genre_query_parser = reqparse.RequestParser()
genre_query_parser.add_argument('page', type=int, help='pagination by 12 items', store_missing=False)
