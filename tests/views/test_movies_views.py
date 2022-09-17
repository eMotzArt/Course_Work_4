import pytest

from app.dao.model import Genre, Director, Movie

class TestMoviesView:
    @pytest.fixture
    def director(self, db):
        obj = Director(name="director")
        db.session.add(obj)
        db.session.commit()
        data = {"id": obj.id, "name": obj.name}
        return data

    @pytest.fixture
    def genre(self, db):
        obj = Genre(name="genre")
        db.session.add(obj)
        db.session.commit()
        data = {"id": obj.id, "name": obj.name}
        return data

    @pytest.fixture
    def movie(self, db, genre, director):
        obj_data = {
            "title": "movie title",
            "description": 'movie description',
            "trailer": 'movie trailer link',
            "year": 2022,
            "rating": 9.9,
            "genre_id": 1,
            "director_id": 1,
        }
        obj = Movie(**obj_data)
        db.session.add(obj)
        db.session.commit()

        data = {"id": obj.id, **obj_data}
        data.update({"genre": {**genre}})
        data.update({"director": {**director}})
        return data


    def test_many(self, client, movie):
        response = client.get("/movies/")
        assert response.status_code == 200
        assert response.json == [movie]

    def test_genre_pages(self, client, movie):
        response = client.get("/movies/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/movies/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_genre(self, client, movie):
        response = client.get("/movies/1/")
        assert response.status_code == 200
        assert response.json == movie

    def test_genre_not_found(self, client, movie):
        response = client.get("/movies/2/")
        assert response.status_code == 404
