from app.dao import MovieDAO


class FavoriteService:

    def __init__(self):
        self.movie_dao = MovieDAO()

    def append_movie_to_favorites(self, movie_id, **kwargs):
        selected_movie = self.movie_dao.get_item(movie_id)
        user = kwargs.get('user')
        user.favorite_movies.append(selected_movie)

    def delete_movie_from_favorites(self, movie_id, **kwargs):
        selected_movie = self.movie_dao.get_item(movie_id)
        user = kwargs.get('user')
        user.favorite_movies.remove(selected_movie)
