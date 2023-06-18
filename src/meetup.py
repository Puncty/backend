from __future__ import annotations

from typing import Optional, Callable
from datetime import datetime
from uuid import uuid4, UUID

from src.user import User
from src.usercollection import UserCollection


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
        if not(admin in self.__members):
            self.__members.append(admin)
        self.datetime = datetime
        self.location = location
        self.id = uuid4() if id is None else UUID(id)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Meetup):
            return self.id == __o.id

        raise NotImplementedError()

    def join(self, user: User) -> None:
        """
        join this meetup

        :param user: the user to join this meetup
        """
        if not self.is_member(user):
            self.__members.append(user)

    def leave(self, user: User) -> None:
        """
        leave this meetup

        :param user: the user to leave this meetup
        """
        if self.is_member(user):
            self.__members.remove(user)
            if self.admin == user and not self.is_empty():
                self.admin = self.__members[0]
            elif self.admin == user:
                self.prunify()

    def prunify(self) -> None:
        """
        edit the meetup in a way that it will be pruned in the next loop
        """
        self.datetime = datetime.now()
        self.location = "Queued for deletion"
        self.id = uuid4()

    def is_member(self, user: User) -> bool:
        """
        check whether a user is a member of this meetup

        :param user: the user to check
        """
        return user in self.__members

    def is_empty(self) -> bool:
        return len(self.__members) == 0

    def to_dict(self, hide_sensitive_information: bool = True, compact: bool = False) -> dict:
        return {
            "id": str(self.id),
            "admin": self.admin.to_dict(hide_sensitive_information) if not compact else str(self.admin.id),
            "members": list(
                map(lambda u: u.to_dict(hide_sensitive_information)
                    if not compact else str(u.id), self.__members)
            ),
            "datetime": int(self.datetime.timestamp()),
            "location": self.location,
        }

    @classmethod
    def from_dict(cls, data: dict, user_collection: UserCollection, compact: bool = False):
        return cls(
            user_collection.by_id(
                data["admin"]["id"] if not compact else data["admin"]),
            datetime.fromtimestamp(data["datetime"]),
            data["location"],
            data["id"],
            [user_collection.by_id(member["id"] if not compact else member)
             for member in data["members"]],
        )
