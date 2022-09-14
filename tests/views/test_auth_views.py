import pytest
from jwt.exceptions import DecodeError, ExpiredSignatureError

from app.utils import Security
from app.dao.model import User



class TestAuthView:
    @pytest.fixture
    def user(self, db):
        obj = User(email=self.user_data.get('email'), password=Security().get_hash(self.user_data.get('password')))
        db.session.add(obj)
        db.session.commit()
        data = {"id": obj.id, "email": obj.name, 'password': obj.password}
        return data

    user_data = {"email": "a@b.c", "password": "test"}
    user_data_wrong_password = {"email": "a@b.c", "password": "wrong_password"}
    user_data_wrong_email = {"email": "wrong", "password": "test"}

    def test_register(self, db, client):
        users_count_before_request = len(db.session.query(User).all())

        response = client.post("/auth/register/", json=self.user_data)

        user = db.session.query(User).first()
        users_count_after_request = len(db.session.query(User).all())

        assert response.status_code == 204
        assert users_count_after_request - users_count_before_request == 1
        assert user.id == 1
        assert user.email == self.user_data.get('email')
        assert user.password == Security().get_hash(self.user_data.get('password'))


    def test_login(self, client, user):
        response = client.post("/auth/login/", json=self.user_data)

        assert response.status_code == 201
        assert 'access_token' in response.json and 'refresh_token' in response.json

    def test_login_wrong_password(self, client, user):
        response = client.post("/auth/login/", json=self.user_data_wrong_password)

        assert response.status_code == 401

    def test_login_wrong_email(self, client, user):
        response = client.post("/auth/login/", json=self.user_data_wrong_email)

        assert response.status_code == 404

    def test_update_by_refresh_token(self, client, user):
        tokens = client.post("/auth/login/", json=self.user_data).json
        response = client.put("auth/login/", json={"refresh_token": tokens.get('refresh_token')})

        assert response.status_code == 201

    def test_update_by_refresh_token_wrong_token(self, client, user):
        client.post("/auth/login/", json=self.user_data)

        with pytest.raises(DecodeError):
            client.put("auth/login/", json={"refresh_token": 'wr.on.g'})

    def test_update_by_refresh_token_expired_token(self, client, user):
        client.post("/auth/login/", json=self.user_data)
        with pytest.raises(ExpiredSignatureError):
            client.put("auth/login/", json={"refresh_token": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFAYi5jIiwidXNlcl9pZCI6MSwiZXhwIjoxNjYzMTU4NDQxfQ.bCiWxyVvNRWu3pbJ_8QwCi958JMwHpud4abtL7WrfrA'})




