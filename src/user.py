from uuid import uuid4
from secrets import token_hex
import bcrypt


class User:
    def __init__(self, name: str, password: str) -> None:
        self.id = uuid4()
        self.name = name
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify(self, pw: str) -> bool:
        return bcrypt.checkpw(pw, self.password)

    def generate_token(self) -> None:
        self.token = token_hex()

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "id": self.id
        }
