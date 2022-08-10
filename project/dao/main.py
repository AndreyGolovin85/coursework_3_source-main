from typing import Optional, List

from sqlalchemy import desc
from werkzeug.exceptions import NotFound

from project.dao.base import BaseDAO, T
from project.models import Genres, Directors, Movies, Users
from project.tools.security import generate_password_hash


class GenresDAO(BaseDAO[Genres]):
    __model__ = Genres


class DirectorsDAO(BaseDAO[Directors]):
    __model__ = Directors


class MoviesDAO(BaseDAO[Movies]):
    __model__ = Movies

    def get_all_f(self, page: Optional[int] = None, filter=None) -> List[T]:
        stmt = self._db_session.query(self.__model__)
        if filter:
            stmt = stmt.order_by(desc(self.__model__.year))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class UsersDAO(BaseDAO[Users]):
    __model__ = Users

    def create(self, email, password):
        try:
            self._db_session.add(
                Users(
                    email=email,
                    password=generate_password_hash(password),
                    name="test",
                    surname="test",
                    favourite_genre="Комедия"
                )
            )
            self._db_session.commit()
            print("Пользователь добавлен")
        except Exception as e:
            print(e)
            self._db_session.rollback()

    def get_user_by_login(self, email):
        try:
            stmt = self._db_session.query(self.__model__).filter(self.__model__.email == email).one()
            return stmt
        except Exception as e:
            print(e)
            return {}

    def update(self, login, data):
        try:
            self._db_session.query(self.__model__).filter(self.__model__.email == login).update(
                data
            )
            self._db_session.commit()
            print("Пользователь обновлен")

        except Exception as e:
            print(e)
            self._db_session.rollback()
