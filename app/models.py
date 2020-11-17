from sqlalchemy import sql, orm
from flask_login import UserMixin
from app import db, login

class State(db.Model):
    __tablename__ = 'state'
    name = db.Column('name', db.String(20), primary_key = True)
    kanye_vote = db.Column('kanye_vote', db.Integer())
    not_kanye_vote = db.Column('not_kanye_vote', db.Integer())

class BlogUser(UserMixin, db.Model):
    __tablename__ = 'bloguser'
    id = db.Column('username', db.String(20), primary_key = True)
    password = db.Column('password', db.String(20))

class BlogPost(db.Model):
    __tablename__ = 'blogpost'
    id = db.Column('id', db.String(20), primary_key = True)
    username = db.Column('username', db.String(20))
    message = db.Column('message', db.String(20))
