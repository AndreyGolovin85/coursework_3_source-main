from flask_restx import fields, Model

from project.setup.api import api

genre: Model = api.model('Жанр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Комедия'),
})

director: Model = api.model('Режисёр', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Квентин Тарантино'),
})


movie: Model = api.model('Фильм', {
    'id': fields.Integer(required=True, example=1),
    'title': fields.String(required=True, max_length=100, example='Рокетмен'),
    'description': fields.String(required=True, max_length=100, example='Рокетмен'),
    'trailer': fields.String(required=True, max_length=100, example='Рокетмен'),
    'year': fields.Integer(required=True, example=2010),
    'rating': fields.Float(required=True, example=10.0),
    'genre': fields.Nested(genre),
    'director': fields.Nested(director),
})

user: Model = api.model('Юзер', {
    'id': fields.Integer(required=True, example=1),
    'name': fields.String(required=True, max_length=100, example='Квентин'),
    'email': fields.String(required=True, max_length=100, example='sdsdff@list.ru'),
    'password': fields.String(required=True, max_length=100, example='ghfs5UY7'),
    'surname': fields.String(required=True, max_length=100, example='Тарантино'),
    'favourite_genre': fields.String(required=True, max_length=100, example='Комедия')
})
