from dataclasses import dataclass
from datetime import datetime
from uuid import  uuid4
from src.user import User


@dataclass
class Meetup:
    def __init__(self, admin: User, datetime: datetime, location: str) -> None:
        self.admin = admin
        self.__members = [admin]
        self.datetime = datetime
        self.location = location
        self.id = uuid4()

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
            "location": self.location
        }
