from flask_restx import Namespace, Resource
from flask import request
from project.container import user_service
from project.setup.api.models import user


api = Namespace('auth')


@api.route('/register/')
class UserRegisterView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self):
        """
        Register user.
        """
        data = request.json
        if data.get("email") and data.get("password"):
            return user_service.create_user(data.get("email"), data.get("password")), 201
        return "Нет почты или пароля", 401


@api.route('/login/')
class UserLoginView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def post(self):
        """
        Logging users.
        """
        data = request.json
        if data.get("email") and data.get("password"):
            print(user_service.check(data.get("email"), data.get("password")))
            return user_service.check(data.get("email"), data.get("password")), 201
        return "Нет почты или пароля", 401

    def put(self):
        req_json = request.json
        print(req_json)
        ref_token = req_json.get("refresh_token")
        if not ref_token:
            return "Токен не задан", 400

        tokens = user_service.update_token(ref_token)
        print(3, tokens)
        if tokens:
            return f"1 {tokens}"
        return "Ошибка в запросе", 400




