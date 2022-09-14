from app.dao import MovieDAO


class MovieService:

    def __init__(self):
        self.dao = MovieDAO()

    def get_movies(self, **params):
        return self.dao.get_items(**params)

    def get_movie_by_pk(self, pk):
        return self.dao.get_item(pk)
