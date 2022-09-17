import pytest
from unittest.mock import patch

from app.dao.model import Genre
from app.service import GenreService


class TestGenreService:

    @pytest.fixture()
    @patch('app.dao.GenreDAO')
    def genre_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_item.return_value = Genre(id=1, name='test_genre')
        dao.get_items.return_value = [
            Genre(id=1, name='test_genre_1'),
            Genre(id=2, name='test_genre_2'),
        ]
        return dao

    @pytest.fixture()
    @patch.object(GenreService, '__init__', lambda self: None)
    def genres_service(self, genre_dao_mock):
        gs = GenreService()
        gs.dao = genre_dao_mock
        return gs

    def test_get_genres(self, genres_service):
        assert len(genres_service.get_genres()) == 2

    def test_get_genre_by_pk(self, genres_service):
        genre = genres_service.get_genre_by_pk(1)
        assert isinstance(genre, Genre)