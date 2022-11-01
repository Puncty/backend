from typing import Optional
from uuid import UUID
from src.meetup import Meetup


class MeetupCollection:
    def __init__(self) -> None:
        self.meetups: list[Meetup] = []

    def append(self, meetup: Meetup) -> None:
        self.meetups.append(meetup)

    def remove(self, meetup: Meetup) -> None:
        self.meetups.remove(meetup)

    def by_id(self, id: UUID) -> Optional[Meetup]:
        for meetup in self.meetups:
            if meetup.id == id:
                return meetup

        return None
