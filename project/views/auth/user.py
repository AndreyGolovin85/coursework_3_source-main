from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        """
        Info user.
        """
        data = request.json
        header = request.headers
        print(header)

        if header:
            return user_service.get_user_by_token(header.get("refresh_token")), 201
        return "Неверный токен", 401

    def patch(self):
        """
        Update user.
        """
        data = request.json
        header = request.headers
        if data:
            return user_service.update_user(data, header.get("refresh_token")), 201
        return "Введите данные", 401


@api.route('/password/')
class UserRefreshPassword(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def put(self):
        """
        Refresh password.
        """
        data = request.json
        header = request.headers
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        if old_password and new_password:
            return user_service.update_password(data, header.get("refresh_token")), 201
        return "Не введен пароль", 401
