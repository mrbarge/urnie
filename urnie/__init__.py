import os

from flask import Flask
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_table import Table, Col

# add DB
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'development':
        app.config.from_object('config.DevelopmentConfig')
    elif app.config['ENV'] == 'test':
        app.config.from_object('config.TestingConfig')

    if 'APP_CONFIG_FILE' in os.environ:
        app.config.from_envvar('APP_CONFIG_FILE')

    from urnie.models import Uri, User

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    migrate.init_app(app, db)

    with app.app_context():
        from urnie.admin.admin import admin_bp
        from urnie.urn.urn import urn_bp
        from urnie.auth.auth import auth_bp

        # add blueprints
        app.register_blueprint(urn_bp, url_prefix='/urn')
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(auth_bp, url_prefix='/auth')

        return app