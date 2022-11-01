from dataclasses import dataclass
from datetime import datetime
from src import User


@dataclass
class Meetup:
    members: list[User]
    datetime: datetime
    location: str

    def to_dict(self) -> dict:
        return {
            "members": map(lambda u: u.to_json(), self.members),
            "datetime": self.datetime.timetuple(),
            "location": self.location
        }
