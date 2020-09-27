import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_table import Table, Col
from flask_bootstrap import Bootstrap
from flask_caching import Cache
from prometheus_flask_exporter import PrometheusMetrics

# add DB
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()
metrics = None

def create_app():
    global metrics
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        app.config.from_object('config.ProductionConfig')
    elif app.config['ENV'] == 'test':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    if 'APP_CONFIG_FILE' in os.environ:
        app.config.from_envvar('APP_CONFIG_FILE')

    from urnie.models import Uri, User

    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    migrate.init_app(app, db)
    metrics = PrometheusMetrics(app)
    bootstrap = Bootstrap(app)

    with app.app_context():
        from urnie.admin.admin import admin_bp
        from urnie.urn.urn import urn_bp
        from urnie.auth.auth import auth_bp
        from urnie.base import base_bp

        # add blueprints
        app.register_blueprint(base_bp, url_prefix='/')
        app.register_blueprint(urn_bp, url_prefix='/urn')
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(auth_bp, url_prefix='/auth')

        return app
