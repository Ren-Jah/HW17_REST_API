from config import db
from marshmallow import Schema, fields


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

    def to_dict(self):
        """Оборачиваем данные фильма в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "trailer": self.trailer,
            "year": self.year,
            "rating": self.rating,
            "genre_id": self.genre_id,
            "genre": self.genre,
            "director_id": self.director_id,
            "director": self.director
        }


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def to_dict(self):
        """Оборачиваем данные режиссера в словарь"""
        return {
            "id": self.id,
            "name": self.name
        }


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def to_dict(self):
        """Оборачиваем данные жанра в словарь"""
        return {
            "id": self.id,
            "name": self.name
        }


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    genre = fields.Nested(GenreSchema(only=('name',)))
    director_id = fields.Int()
    director = fields.Nested(DirectorSchema(only=('name',)))