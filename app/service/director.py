from app.dao import DirectorDAO


class DirectorService:

    def __init__(self):
        self.dao = DirectorDAO()

    def get_directors(self, **params):
        return self.dao.get_items(**params)

    def get_director_by_pk(self, pk):
        return self.dao.get_item(pk)
