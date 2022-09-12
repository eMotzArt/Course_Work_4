from app.dao import GenreDAO


class GenreService:

    def __init__(self):
        self.dao = GenreDAO()

    def get_genres(self):
        return self.dao.get_items()

    def get_genre_by_pk(self, pk):
        return self.dao.get_item(pk)

