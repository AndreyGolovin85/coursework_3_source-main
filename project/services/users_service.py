from typing import Optional, List

from project.dao import UsersDAO
from project.exceptions import ItemNotFound
from project.models import Users
from project.tools.security import AuthService, generate_password_hash


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Users:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> List[Users]:
        return self.dao.get_all(page=page)

    def create_user(self, email, password):
        self.dao.create(email, password)

    def get_user_by_login(self, email):
        return self.dao.get_user_by_login(email)

    def check(self, email, password):
        user = self.get_user_by_login(email)
        email = user.email
        password_hash = user.password
        return AuthService.generate_tokens(email, password, password_hash)

    def update_token(self, refresh_token):
        return AuthService.approve_refresh_token(refresh_token)

    def get_user_by_token(self, refresh_token):
        data = AuthService.get_data_user_from_token(refresh_token)
        if data:
            return self.get_user_by_login(data.get("email"))

    def update_user(self, data: dict, refresh_token):
        user = self.get_user_by_token(refresh_token)
        if user:
            self.dao.update(user.email, data)

    def update_password(self, data, refresh_token):
        user = self.get_user_by_token(refresh_token)
        email = user.email
        password_hash = user.password
        if password_hash == generate_password_hash(data.get("old_password")):
            print("Пароли совпадают")
            new_password_hash = generate_password_hash(data.get("new_password"))
            self.dao.update(user.email, {"password": new_password_hash})
            return self.check(email, data.get("new_password"))
        return "Введен неверный пароль"
