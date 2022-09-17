import pytest
from app.utils import Security
from app.dao.model import User, Director, Genre, Movie



class TestFavoritesView:
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

    user_data = {"email": "a@b.c", "password": "test"}

    @pytest.fixture
    def user_add_fav_movie(self, client, tokens):
        access_token = tokens.get('access_token')
        client.post("/favorites/movies/1/", headers={"Authorization": f"Bearer {access_token}"})

    @pytest.fixture
    def user_create(self, client):
        client.post("/auth/register/", json=self.user_data)

    @pytest.fixture
    def tokens(self, client, user_create):
        response = client.post("/auth/login/", json=self.user_data)
        return response.json

#get
    def test_get_fav_movie_user_zero(self, client, tokens):
        access_token = tokens.get('access_token')
        response = client.get("/favorites/movies/", headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 200
        assert len(User.query.first().favorite_movies) == 0

    def test_get_fav_movie_user_one(self, client, tokens, movie, user_add_fav_movie):
        access_token = tokens.get('access_token')
        response = client.get("/favorites/movies/", headers={"Authorization": f"Bearer {access_token}"})

        assert response.status_code == 200
        assert len(User.query.first().favorite_movies) == 1
#post
    def test_add_fav_movie_to_user(self, client, tokens, movie):
        user_favorite_movies__before_count = len(User.query.first().favorite_movies)
        access_token = tokens.get('access_token')
        response = client.post("/favorites/movies/1/", headers={"Authorization": f"Bearer {access_token}"})
        user_favorite_movies_after_count = len(User.query.first().favorite_movies)
        assert response.status_code == 204
        assert user_favorite_movies_after_count  > user_favorite_movies__before_count
#delete
    def test_del_fav_movie_from_user(self, client, tokens, movie, user_add_fav_movie):
        user_favorite_movies__before_count = len(User.query.first().favorite_movies)
        access_token = tokens.get('access_token')
        response = client.delete("/favorites/movies/1/", headers={"Authorization": f"Bearer {access_token}"})
        user_favorite_movies_after_count = len(User.query.first().favorite_movies)
        assert response.status_code == 204
        assert user_favorite_movies_after_count < user_favorite_movies__before_count

