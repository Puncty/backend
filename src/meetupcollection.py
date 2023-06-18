from __future__ import annotations

import threading
from copy import deepcopy
from datetime import datetime
from typing import Optional, Callable
from uuid import UUID
from src.meetup import Meetup
from src.user import User
from src.utility.generics import get_first_match, get_all_matches
from src.utility.storage import Storage
from src.usercollection import UserCollection


class MeetupCollection:
    def __init__(self, meetups: Optional[list[Meetup]] = None, on_mutation: Callable[[MeetupCollection], None] = lambda _: None) -> None:
        self.__meetups: list[Meetup] = [] if meetups is None else meetups
        self.on_mutation: Callable[[MeetupCollection], None] = on_mutation

        # prune every half hour
        threading.Thread(target=self.__prune_loop, args=[30 * 60]).start()

    def __prune_loop(self, interval_seconds: float):
        print("Pruning...")
        self.__prune()
        threading.Timer(interval_seconds, function=self.__prune_loop,
                        args=[interval_seconds]).start()

    def __prune(self):
        now = datetime.now()
        count = 0
        for meetup in [m for m in self.__meetups]:
            if now > meetup.datetime:
                self.__meetups.remove(meetup)
                count += 1
        self.on_mutation(self)
        print(f"Pruned {count} Meetups")

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

    def to_dict(self, hide_sensitive_information: bool = True, compact: bool = False) -> dict:
        return {
            "meetups": [
                meetup.to_dict(hide_sensitive_information, compact) for meetup in self.__meetups
            ]
        }

    @ classmethod
    def from_dict(cls, data: dict, uc: UserCollection, on_mutation: Callable[[MeetupCollection], None], compact: bool = False):
        return cls([Meetup.from_dict(meetup, uc, compact) for meetup in data["meetups"]], on_mutation=on_mutation)

    @ classmethod
    def load(cls, storage: Storage, uc: UserCollection, on_mutation: Callable[[MeetupCollection], None]):
        return cls(on_mutation=on_mutation)  \
            if not storage.has("meetup-collection") \
            else cls.from_dict(storage["meetup-collection"], uc, on_mutation=on_mutation, compact=True)
