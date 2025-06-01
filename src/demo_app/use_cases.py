from dataclasses import dataclass

from .dao import UserDAO, LinkDAO
from .protocols import TransactionManager


@dataclass
class NewUser:
    name: str
    links: list[str]


class UserService:
    def __init__(
            self,
            user_dao: UserDAO,
            link_dao: LinkDAO,
            transaction_manager: TransactionManager,
    ):
        self.user_dao = user_dao
        self.link_dao = link_dao
        self.transaction_manager = transaction_manager

    async def create_user(self, input_data: NewUser) -> int:
        user_id = self.user_dao.add_user(input_data.name)
        for link in input_data.links:
            self.link_dao.add_link(user_id, link)
        self.transaction_manager.commit()
        return user_id
