import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'changeme'


class ProductionConfig(Config):
    if 'SECRET_KEY' in os.environ:
        SECRET_KEY = os.environ['SECRET_KEY']
    if 'DATABASE_URI' in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']


class DevelopmentConfig(Config):
    DEBUG = True
    if 'DATABASE_URI' in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    REDIS_URL = "redis://:password@localhost:6379/0"


class TestingConfig(Config):
    TESTING = True
    REDIS_URL = "redis://:password@localhost:6379/0"
