from __future__ import annotations

from typing import Optional, Callable
from uuid import UUID
from src.user import User
from src.utility.generics import get_first_match
from src.utility.storage import Storage


class UserCollection:
    def __init__(self, users: list[User] = [], on_mutation: Callable[[UserCollection], None] = lambda _: None) -> None:
        self.__users: list[User] = users
        self.on_mutation: Callable[[UserCollection], None] = on_mutation

    def append(self, user: User) -> None:
        self.__users.append(user)
        self.on_mutation(self)

    def remove(self, user: User) -> None:
        self.__users.remove(user)
        self.on_mutation(self)

    def by_id(self, id: str | UUID) -> Optional[User]:
        if type(id) is str:
            try:
                id = UUID(id)
            except:
                return None
        return get_first_match(lambda x: x.id == id, self.__users)

    def by_email_address(self, email_address: str) -> Optional[User]:
        return get_first_match(lambda x: x.email_address == email_address.lower(), self.__users)

    def to_dict(self, hide_sensitive_information: bool = True) -> dict:
        return {
            "users": [user.to_dict(hide_sensitive_information) for user in self.__users]
        }

    @classmethod
    def from_dict(cls, data: dict, on_mutation: Callable[[UserCollection], None]):
        return cls([User.from_dict(user) for user in data["users"]], on_mutation=on_mutation)

    @classmethod
    def load(cls, storage: Storage, on_mutation: Callable[[UserCollection], None]):
        return cls(on_mutation=on_mutation) if not storage.has("user-collection") else cls.from_dict(storage["user-collection"], on_mutation=on_mutation)
