from app.dao import DirectorDAO


class DirectorService:

    def __init__(self):
        self.dao = DirectorDAO()

    def get_directors(self):
        return self.dao.get_items()

    def get_director_by_pk(self, pk):
        return self.dao.get_item(pk)

    def add_new_director(self, **data):
        return self.dao.create_item(**data)

    def update_director(self, pk, **data):
        return self.dao.update_item(pk, **data)

    def delete_director(self, pk):
        return self.dao.delete_item(pk)
