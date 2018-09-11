from magina import db, login_manager
from flask_login import UserMixin


class Keyword(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(20), nullable=False, unique=True, index=True)


class Choice(db.Model):
    __tablename__ = 'choices'
    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True, index=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
