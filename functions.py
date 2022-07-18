from model_manager import Movie, Director, Genre
from config import db
import json


def insert_data_universal(model, input_data):
    """Универсальная функция для добавления данных в зависимости от модели"""
    for row in input_data:
        db.session.add(
            model(
                **row
            )
        )

    db.session.commit()


def init_db():
    """Функция для загрузки данных из JSON"""
    db.drop_all()
    db.create_all()
    with open("data/movie.json", encoding="UTF-8") as file:
        insert_data_universal(Movie, json.load(file))

    with open("data/directors.json", encoding="UTF-8") as file:
        insert_data_universal(Director, json.load(file))

    with open("data/genres.json", encoding="UTF-8") as file:
        insert_data_universal(Genre, json.load(file))