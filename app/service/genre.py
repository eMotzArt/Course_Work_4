from app.dao import GenreDAO


class GenreService:

    def __init__(self):
        self.dao = GenreDAO()

    def get_genres(self):
        return self.dao.get_items()

    def get_genre_by_pk(self, pk):
        return self.dao.get_item(pk)

    def add_new_genre(self, **data):
        return self.dao.create_item(**data)

    def update_genre(self, pk, **data):
        return self.dao.update_item(pk, **data)

    def delete_genre(self, pk):
        return self.dao.delete_item(pk)
