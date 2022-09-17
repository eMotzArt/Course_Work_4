import pytest
from unittest.mock import patch

from app.dao.model import User, Movie
from app.service import FavoriteService


class TestUserService:
    @pytest.fixture
    def user_empty(self):
        g = User(id=1, email="user 1", password='password1')
        return g

    @pytest.fixture
    def user_with_fav_movie(self, movie):
        g = User(id=1, email="user 1", password='password1')
        g.favorite_movies.append(movie)
        return g

    @pytest.fixture()
    def movie(self):
        movie_data = {
            'id': 1,
            'title': 'Movie title',
            'description': 'Movie description',
            'trailer': 'Movie trailer link',
            'year': 2022,
            'rating': 9.9,
            'genre_id': 2,
            'director_id': 2
        }
        movie = Movie(**movie_data)
        return movie

    @pytest.fixture
    @patch('app.dao.MovieDAO')
    def movie_dao_mock(self, movie_dao_mock, movie):
        dao = movie_dao_mock()
        dao.get_item.return_value = movie
        return dao

    @pytest.fixture()
    @patch.object(FavoriteService, '__init__', lambda self: None)
    def favorite_service(self, movie_dao_mock):
        fs = FavoriteService()
        fs.movie_dao = movie_dao_mock
        return fs

    def test_append_movie_to_favorites(self, favorite_service, user_empty):
        assert len(user_empty.favorite_movies) == 0
        favorite_service.append_movie_to_favorites(1, user=user_empty)
        assert len(user_empty.favorite_movies) == 1
        new_favorite_movie = user_empty.favorite_movies[0]
        assert isinstance(new_favorite_movie, Movie)
        assert new_favorite_movie.title == 'Movie title'

    def test_delete_movie_from_favorites(self, favorite_service, user_with_fav_movie, movie):
        assert len(user_with_fav_movie.favorite_movies) == 1
        favorite_service.delete_movie_from_favorites(1, user=user_with_fav_movie)
        assert len(user_with_fav_movie.favorite_movies) == 0