import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    if 'SECRET_KEY' in os.environ:
        SECRET_KEY = os.environ['SECRET_KEY']
    if 'DATABASE_URI' in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    # Maximum number of pending URNs before suggestions are disallowed
    MAX_PENDING_URNS = 30
    # Cache URN requests, default to in-memory
    CACHE_TYPE = 'simple'
    # Cache URN requests for the specified number of seconds
    CACHE_DEFAULT_TIMEOUT = 300


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
