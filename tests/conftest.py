import pytest

from app.config import TestingConfig
from app.app import create_app
from app.database import db as database
from app.views import api


@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        api.init_app(app)
        yield app


@pytest.fixture
def db(app):
    database.init_app(app)
    database.drop_all()
    database.create_all()
    database.session.commit()
    yield database

    database.session.close()


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        yield client
