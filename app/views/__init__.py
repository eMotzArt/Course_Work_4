__all__ = ['api']
from flask_restx import Api

from .genres_api.genres_api import api as genres_api
from .directors_api.directors_api import api as directors_api
from .movies_api.movies_api import api as movies_api
from .users_api.users_api import api as users_api
from .auth_api.auth_api import api as auth_api
from .favorites_api.favorites_api import api as fav_api


api = Api(
    authorizations={
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    title="Flask Course Project 3",
    doc="/docs",
)

api.add_namespace(genres_api)
api.add_namespace(directors_api)
api.add_namespace(movies_api)
api.add_namespace(users_api)
api.add_namespace(auth_api)
api.add_namespace(fav_api)