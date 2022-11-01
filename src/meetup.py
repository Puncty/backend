from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src import User


@dataclass
class Meetup:
    members: list[User]
    datetime: datetime
    location: str
    id: UUID

    def to_dict(self) -> dict:
        return {
            "members": map(lambda u: u.to_json(), self.members),
            "datetime": self.datetime.timetuple(),
            "location": self.location
        }
