import base64
import hashlib
import calendar
import datetime

import jwt

from flask import current_app
from flask_restx import abort


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')

# TODO: [security] Описать функцию compose_passwords(password_hash: Union[str, bytes], password: str)


def compare_hash(password, password_hash):
    return password_hash == generate_password_hash(password)


class AuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    @staticmethod
    def generate_tokens(email, password, password_hash, is_refresh=False):

        if not is_refresh:
            if compare_hash(password, password_hash):
                print("Что-то не так")
                raise abort(400)

        data = {
            "email": email,
            "password": password
        }

        # Создание токена на 15 минут.
        min_15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        data["exp"] = calendar.timegm(min_15.timetuple())
        access_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['JWT_ALG'])

        # Обновление, 130 дней
        days_130 = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
        data["exp"] = calendar.timegm(days_130.timetuple())
        refresh_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['JWT_ALG'])

        return {"access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    def approve_refresh_token(refresh_token):
        data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                          algorithms=current_app.config['JWT_ALG'])
        email = data.get("email")
        password = data.get("password")

        if not email:
            return False

        return AuthService.generate_tokens(email, password, generate_password_hash(password), is_refresh=True)

    @staticmethod
    def get_data_user_from_token(refresh_token):
        data = jwt.decode(jwt=refresh_token, key=current_app.config['SECRET_KEY'],
                          algorithms=current_app.config['JWT_ALG'])
        return data


