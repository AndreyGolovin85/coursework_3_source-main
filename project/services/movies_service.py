from typing import Optional, List

from project.dao import MoviesDAO
from project.exceptions import ItemNotFound
from project.models import Movies


class MoviesService:
    def __init__(self, dao: MoviesDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Movies:
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'Movie with pk={pk} not exists.')

    def get_all(self, filter=None, page: Optional[int] = None) -> List[Movies]:
        return self.dao.get_all_f(page=page, filter=filter)
