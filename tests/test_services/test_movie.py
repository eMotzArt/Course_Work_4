import pytest
from unittest.mock import patch
from app.service import MovieService

class TestMovieService:
    @pytest.fixture(autouse=True)
    @patch.object(MovieService, '__init__', lambda self: None)
    def genre_service(self, movie_dao):
        self.movie_service = MovieService()
        self.movie_service.dao = movie_dao

    def test_get_movies(self):
        all_movies = self.movie_service.get_movies()
        assert len(all_movies) > 0

    def test_get_movie_by_pk(self):
        movie = self.movie_service.get_movie_by_pk(1)
        expected_movie_data = {
            'title': "title_1",
            'description': 'desc_1',
            'trailer': 'youtube_1',
            'year': 1991,
            'rating': 6.6,
            'genre_id': 1,
            'director_id': 1
        }
        assert movie is not None
        assert movie.id == 1
        for key, value in expected_movie_data.items():
            movie_value = getattr(movie, key)
            assert movie_value == value

    def test_add_new_movie_with_names(self):
        new_movie_data = {
            'title': "title_5",
            'description': 'desc_5',
            'trailer': 'youtube_5',
            'year': 1995,
            'rating': 10.0,
            'genre_name': 'Комедия',
            'director_name': 'Пол Шерридан'
        }
        new_movie = self.movie_service.add_new_movie_with_names(**new_movie_data)
        assert new_movie is not None
        assert new_movie.id is not None
        del new_movie_data['genre_name']
        del new_movie_data['director_name']
        for key, value in new_movie_data.items():
            movie_value = getattr(new_movie, key)
            assert movie_value == value
        assert new_movie.genre_id is not None
        assert new_movie.director_id is not None

    def test_add_new_movie(self):
        new_movie_data = {
            'title': "title_4",
            'description': 'desc_4',
            'trailer': 'youtube_4',
            'year': 1994,
            'rating': 9.9,
            'genre_id': 4,
            'director_id': 4
        }
        new_movie = self.movie_service.add_new_movie(**new_movie_data)
        assert new_movie is not None
        assert new_movie.id is not None
        for key, value in new_movie_data.items():
            movie_value = getattr(new_movie, key)
            assert movie_value == value

    def test_update_movie(self):
        data = {
            'id': 2,
            'title': "new_title",
            'description': 'new_desc',
            'trailer': 'new_tube',
            'year': 1990,
            'rating': 0.1,
            'genre_id': 5,
            'director_id': 5
        }
        movie = self.movie_service.update_movie(2, **data)
        assert movie is not None
        for key, value in data.items():
            movie_value = getattr(movie, key)
            assert movie_value == value



    def test_delete_movie(self):
        self.movie_service.delete_movie(2)