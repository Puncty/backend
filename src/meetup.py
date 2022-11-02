from typing import Optional
from datetime import datetime
from uuid import uuid4, UUID

from src.user import User
from src.globals import user_collection


class Meetup:
    def __init__(
        self,
        admin: User,
        datetime: datetime,
        location: str,
        id: Optional[UUID] = None,
        members: Optional[list[User]] = None,
    ) -> None:
        self.admin = admin
        self.__members = [admin] if members is None else members
        self.datetime = datetime
        self.location = location
        self.id = uuid4() if id is None else id

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Meetup):
            return self.id == __o.id

        raise NotImplementedError()

    def join(self, user: User) -> None:
        self.__members.append(user)

    def leave(self, user: User) -> None:
        self.__members.remove(user)

    def is_member(self, user: User) -> bool:
        return user in self.__members

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "admin": self.admin.to_dict(),
            "members": list(map(lambda u: u.to_dict(), self.__members)),
            "datetime": int(self.datetime.timestamp()),
            "location": self.location,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            user_collection.by_id(data["admin"]["id"]),
            datetime.fromtimestamp(data["datetime"]),
            data["location"],
            data["id"],
            [user_collection.by_id(member["id"]) for member in data["members"]],
        )
