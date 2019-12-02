from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


DATABASE_URI = os.getenv('DATABASE_URI')
db = SQLAlchemy()


def setup_db(app, database_path=DATABASE_URI):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
   


# Helper table

movies = db.Table('movies', db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'), primary_key=True),
                  db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True))

# Actor


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    movies = db.relationship('Movie', secondary=movies,
                             lazy='dynamic', backref=db.backref('actors'))

    def attributes(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

# Movie


class Movie(db.Model):
    __tablename = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    release_date = db.Column(db.DateTime())

    def attributes(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
