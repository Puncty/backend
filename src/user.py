from typing import Optional
from uuid import uuid4, UUID
from secrets import token_hex
import bcrypt


class User:
    def __init__(self, name: str, password: str, email_address: str, id: Optional[UUID] = None) -> None:
        self.id = uuid4() if id is None else id
        self.name = name
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.email_address = email_address

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, User):
            return self.id == __o.id

        raise NotImplementedError()

    def verify(self, pw: str) -> bool:
        return bcrypt.checkpw(pw.encode(), self.password)

    def generate_token(self) -> None:
        self.token = token_hex()

    def to_dict(self) -> dict:
        return {"name": self.name, "id": self.id, "email_address": self.email_address}
