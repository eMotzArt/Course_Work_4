from flask import Flask, g
from app.views import api
from app.database import db
from flask_cors import CORS

def create_app(config):
    new_app = Flask(__name__)
    new_app.config.from_object(config)
    new_app.app_context().push()

    @new_app.before_request
    def create_session():
        """Перед каждым запросом кладет сессию в g"""
        g.session = db.session

    @new_app.after_request
    def close_session(response):
        try:
            g.session.commit()
        except:
            g.session.rollback()
        finally:
            g.session.close()
        return response

    return new_app

def config_app(app):
    CORS(app=app)
    db.init_app(app)
    api.init_app(app)
