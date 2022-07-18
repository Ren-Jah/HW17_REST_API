from flask import Flask, request
from config import db, app, api
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from model_manager import Movie, Director, Genre, MovieSchema
from functions import init_db

movies_ns = api.namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# Вьюшка с отображением фильмов с учетом возможной фильтрации по режиссеру и/или жанру
@movies_ns.route("/")
class MoviesView(Resource):
    def get(self):
        all_movies_query = db.session.query(Movie)

        director_id = request.args.get("director_id")
        if director_id:
            all_movies_query = all_movies_query.filter(Movie.director_id == director_id)

        genre_id = request.args.get("genre_id")
        if genre_id:
            all_movies_query = all_movies_query.filter(Movie.genre_id == genre_id)

        final_query = all_movies_query.all()

        return movies_schema.dump(final_query), 200

    def post(self):
        new_data = request.json

        movie = movie_schema.load(new_data)
        new_movie = Movie(**movie)
        with db.session.begin():
            db.session.add(new_movie)

        return "Created", 201


# Вьюшка отображает полную информацию по фильму по выбранному id
@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    def get(self, mid):
        movie = Movie.query.get(mid)

        if not movie:
            return "Not found", 404

        return movie_schema.dump(movie), 200

    def put(self, mid):
        movie_selected = db.session.query(Movie).filter(Movie.id == mid)
        movie_first = movie_selected.first()

        if movie_first is None:
            return "Not found", 404

        new_data = request.json
        movie_selected.update(new_data)
        db.session.commit()

        return "No Content", 204

    def delete(self, mid):
        movie_selected = db.session.query(Movie).filter(Movie.id == mid)
        movie_first = movie_selected.first()

        if movie_first is None:
            return "Not found", 404

        rows_deleted = movie_selected.delete()

        # если произошло удаление более 1 строки, то указываем на наличие проблемы.
        if rows_deleted != 1:
            return "bad request", 400

        db.session.commit()
        return "No Content", 204


if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=8000, debug=True)