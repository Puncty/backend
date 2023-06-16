from __future__ import annotations

from typing import Optional, Callable
from uuid import UUID
from src.meetup import Meetup
from src.user import User
from src.utility.generics import get_first_match, get_all_matches


class MeetupCollection:
    def __init__(self, meetups: Optional[list[Meetup]] = None, on_mutation: Callable[[MeetupCollection], None] = lambda _: None) -> None:
        self.__meetups: list[Meetup] = [] if meetups is None else meetups
        self.on_mutation: Callable[[MeetupCollection], None] = on_mutation

    def append(self, meetup: Meetup) -> None:
        self.__meetups.append(meetup)
        self.on_mutation(self)

    def remove(self, meetup: Meetup) -> None:
        self.__meetups.remove(meetup)
        self.on_mutation(self)

    def by_id(self, id: UUID) -> Optional[Meetup]:
        if type(id) is str:
            try:
                id = UUID(id)
            except:
                return None

        return get_first_match(lambda m: m.id == id, self.__meetups)

    def with_member(self, user: User) -> list[Meetup]:
        return get_all_matches(lambda m: m.is_member(user), self.__meetups)

    def to_dict(self, hide_sensitive_information: bool = True) -> dict:
        return {
            "meetups": [
                meetup.to_dict(hide_sensitive_information) for meetup in self.__meetups
            ]
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls([Meetup.from_dict(meetup) for meetup in data["meetups"]])
