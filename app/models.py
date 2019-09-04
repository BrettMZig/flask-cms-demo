from .main import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import re


db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(1000), index=True)
    title = db.Column(db.String(1000))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, title, content):
        self.title = title
        self.slug = re.sub(r'[^\w]+', '-', title.lower())
        self.content = content

    def __repr__(self):
        return '<Pages : id=%r, title=%s, slug=%s>' \
              % (self.id, self.title, self.slug)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, plain_text_password):
        self.username = username
        self.password_hash = generate_password_hash(plain_text_password)

    def set_password(self, plain_text_password):
        self.password_hash = generate_password_hash(plain_text_password)

    def check_password(self, plain_text_password):
        return check_password_hash(self.password_hash, plain_text_password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
