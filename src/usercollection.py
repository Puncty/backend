from typing import Optional
from uuid import UUID
from src.user import User


class UserCollection:
    def __init__(self) -> None:
        self.users: list[User] = []

    def append(self, user: User) -> None:
        self.users.append(user)

    def remove(self, user: User) -> None:
        self.users.remove(user)

    def by_id(self, id: UUID) -> Optional[User]:
        for user in self.users:
            if user.id == id:
                return user

        return None
