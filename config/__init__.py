import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    if 'SECRET_KEY' in os.environ:
        SECRET_KEY = os.environ['SECRET_KEY']
    if 'DATABASE_URI' in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_URL = "redis://:password@localhost:6379/0"


class TestingConfig(Config):
    TESTING = True
    REDIS_URL = "redis://:password@localhost:6379/0"
