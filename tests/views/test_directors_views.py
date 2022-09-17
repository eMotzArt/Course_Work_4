import pytest

from app.dao.model import Director


class TestDirectorsView:
    @pytest.fixture
    def director(self, db):
        obj = Director(name="director")
        db.session.add(obj)
        db.session.commit()
        data = {"id": obj.id, "name": obj.name}
        return data

    def test_many(self, client, director):
        response = client.get("/directors/")
        assert response.status_code == 200
        assert response.json == [director]

    def test_genre_pages(self, client, director):
        response = client.get("/directors/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/directors/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_genre(self, client, director):
        response = client.get("/directors/1/")
        assert response.status_code == 200
        assert response.json == director

    def test_genre_not_found(self, client, director):
        response = client.get("/directors/2/")
        assert response.status_code == 404
