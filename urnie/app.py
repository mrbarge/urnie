from flask import Flask
from flask_redis import FlaskRedis

from admin.admin import admin_bp
from urn.urn import urn_bp

app = Flask(__name__)

if app.config['ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')
elif app.config['ENV'] == 'test':
    app.config.from_object('config.TestingConfig')

app.config.from_envvar('APP_CONFIG_FILE')

# add blueprints
app.register_blueprint(urn_bp, url_prefix='/urn')
app.register_blueprint(admin_bp, url_prefix='/admin')

# add redis
redis_client = FlaskRedis(app)

if __name__ == '__main__':
    app.run()