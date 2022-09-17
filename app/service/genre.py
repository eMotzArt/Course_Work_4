from app.dao import GenreDAO


class GenreService:

    def __init__(self):
        self.dao = GenreDAO()

    def get_genres(self, **params):
        return self.dao.get_items(**params)

    def get_genre_by_pk(self, pk):
        return self.dao.get_item(pk)

