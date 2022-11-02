from typing import Optional
from uuid import UUID
from src.meetup import Meetup
from src.utility.generics import get_first_match


class MeetupCollection:
    def __init__(self, meetups: Optional[list[Meetup]] = None) -> None:
        self.__meetups: list[Meetup] = [] if meetups is None else meetups

    def append(self, meetup: Meetup) -> None:
        self.__meetups.append(meetup)

    def remove(self, meetup: Meetup) -> None:
        self.__meetups.remove(meetup)

    def by_id(self, id: UUID) -> Optional[Meetup]:
        if type(id) is str:
            try:
                id = UUID(id)
            except:
                return None

        return get_first_match(lambda x: x.id == id, self.__meetups)

    def to_dict(self, hide_sensitive_information: bool = True) -> dict:
        return {
            "meetups": [
                meetup.to_dict(hide_sensitive_information) for meetup in self.__meetups
            ]
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls([Meetup.from_dict(meetup) for meetup in data["meetups"]])
