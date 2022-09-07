import pytest
from unittest.mock import patch
from app.service import GenreService

class TestGenreService:
    @pytest.fixture(autouse=True)
    @patch.object(GenreService, '__init__', lambda self: None)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService()
        self.genre_service.dao = genre_dao

    def test_get_genres(self):
        all_genres = self.genre_service.get_genres()
        assert len(all_genres) > 0

    def test_get_genre_by_pk(self):
        genre = self.genre_service.get_genre_by_pk(1)
        assert genre is not None
        assert genre.id == 1
        assert genre.name == 'Комедия'

    def test_add_new_genre(self):
        data = {'name':  'Мюзикл'}
        new_genre = self.genre_service.add_new_genre(**data)
        assert new_genre is not None
        assert new_genre.id is not None
        assert new_genre.name == data['name']


    def test_update_genre(self):
        data = {'name':  'Комедия'}
        genre = self.genre_service.update_genre(1, **data)
        assert genre is not None
        assert genre.id == 1
        assert genre.name == data['name']

    def test_delete_genre(self):
        self.genre_service.delete_genre(1)
