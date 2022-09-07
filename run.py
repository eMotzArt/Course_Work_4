from app import create_app, config_app
from app import Config

if __name__ == '__main__':
    app = create_app(Config())
    config_app(app)
    app.run(host="localhost", port=5000)
    #commit