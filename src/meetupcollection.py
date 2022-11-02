from typing import Optional
from uuid import UUID
from src.meetup import Meetup
from src.utility.generics import get_first_match


class MeetupCollection:
    def __init__(self) -> None:
        self.meetups: list[Meetup] = []

    def append(self, meetup: Meetup) -> None:
        self.meetups.append(meetup)

    def remove(self, meetup: Meetup) -> None:
        self.meetups.remove(meetup)

    def by_id(self, id: UUID) -> Optional[Meetup]:
        if type(id) is str:
            id = UUID(id)

        return get_first_match(lambda x: x.id == id, self.meetups)
