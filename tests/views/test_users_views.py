import pytest
from app.utils import Security
from app.dao.model import User



class TestUsersView:
    user_data = {"email": "a@b.c", "password": "test"}

    @pytest.fixture
    def user_create(self, client):
        client.post("/auth/register/", json=self.user_data)

    @pytest.fixture
    def tokens(self, client, user_create):
        response = client.post("/auth/login/", json=self.user_data)
        return response.json

#get
    def test_get_user(self, client, tokens):
        access_token = tokens.get('access_token')
        response = client.get("/user/", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

    def test_get_user_no_headers(self, client, tokens):
        response = client.get("/user/")
        assert response.status_code == 401

    def test_get_user_invalid_token(self, client, user_create):
        response = client.get("/user/", headers={"Authorization": "Bearer a.b.c"})
        assert response.status_code == 401

    def test_get_user_expired_token(self, client, user_create):
        response = client.get("/user/", headers={"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFAYi5jIiwidXNlcl9pZCI6MSwiZXhwIjoxNjYzMTU4NDQxfQ.bCiWxyVvNRWu3pbJ_8QwCi958JMwHpud4abtL7WrfrA"})
        assert response.status_code == 401

#patch
    def test_update_user_info(self, client, tokens):
        new_data = {'favourite_genre': 4, 'name': 'new_name'}
        access_token = tokens.get('access_token')
        response = client.patch("/user/", json=new_data, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 204

        user = User.query.first()
        assert user.favorite_genre == new_data.get('favourite_genre')
        assert user.name == new_data.get('name')

#put
    def test_update_user_password(self, db, client, tokens):
        passwords = {'old_password': 'test', 'new_password': 'new_test_password'}
        access_token = tokens.get('access_token')
        response = client.put("/user/password/", json=passwords, headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 204

        user = User.query.first()
        new_password = passwords.get('new_password')
        new_password_hash = Security().get_hash(new_password)
        assert user.password == new_password_hash

    def test_update_user_password_wrong_password(self, db, client, tokens):
        passwords = {'old_password': 'wrong', 'new_password': 'new_test_password'}
        access_token = tokens.get('access_token')
        response = client.put("/user/password/", json=passwords,
                              headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 400

