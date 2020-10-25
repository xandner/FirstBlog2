import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    FLASK_ENV=os.getenv('FLASK_ENV')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY=os.getenv('SECRET_KEY')
    REDIS_SERVER_URL = os.getenv('REDIS_SERVER_URL')


class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
