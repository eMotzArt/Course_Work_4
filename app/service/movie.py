from app.dao import MovieDAO


class MovieService:

    def __init__(self):
        self.dao = MovieDAO()


    def get_movies(self, **params):
        if not params:
            return self.dao.get_items()
        return self.dao.get_items_with_filtering(**params)

    def get_movie_by_pk(self, pk):
        return self.dao.get_item(pk)

    def add_new_movie_with_names(self, **data):
        return self.dao.add_movie_with_names(**data)

    def add_new_movie(self, **data):
        return self.dao.create_item(**data)

    def update_movie(self, pk, **data):
        return self.dao.update_item(pk, **data)

    def delete_movie(self, pk):
        return self.dao.delete_item(pk)
