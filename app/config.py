class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/database.db?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSON_AS_ASCII = False
    DEBUG = True
