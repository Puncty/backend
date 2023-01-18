from typing import Optional
from uuid import UUID
from src.user import User
from src.utility.generics import get_first_match
from src.data import Data


class UserCollection:
    def __init__(self) -> None:
        self.__users: list[User] = []

    def append(self, user: User) -> None:
        self.__users.append(user)
        Data.get().write("user-collection", self.to_dict())

    def remove(self, user: User) -> None:
        self.__users.remove(user)
        Data.get().write("user-collection", self.to_dict())

    def by_id(self, id: str | UUID) -> Optional[User]:
        if type(id) is str:
            try:
                id = UUID(id)
            except:
                return None
        return get_first_match(lambda x: x.id == id, self.__users)

    def by_email_address(self, email_address: str) -> Optional[User]:
        return get_first_match(lambda x: x.email_address == email_address, self.__users)

    def to_dict(self, hide_sensitive_information: bool = True) -> dict:
        return {
            "users": [user.to_dict(hide_sensitive_information) for user in self.__users]
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls([User.from_dict(user) for user in data["users"]])

    @classmethod
    def load(cls):
        try:
            return cls.from_dict(Data.get().read()["user-collection"])
        except:
            return cls()
