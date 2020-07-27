from flask_login import UserMixin
from . import db, login_manager
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Uri(db.Model):
    __tablename__ = 'uri'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(30), unique=True, nullable=False)
    url = db.Column(db.String(200), unique=False, nullable=False)
    approved = db.Column(db.Boolean, unique=False, nullable=False)
    date_added = db.Column(db.DateTime, unique=False, nullable=True)

    def __init__(self, key, url, approved):
        self.key = key
        self.url = url
        self.approved = approved

    def __repr__(self):
        return '<id {}>'.format(self.id)
