class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_URL = "redis://:password@localhost:6379/0"

class TestingConfig(Config):
    TESTING = True
    REDIS_URL = "redis://:password@localhost:6379/0"
