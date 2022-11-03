from typing import Optional
from uuid import uuid4, UUID
from secrets import token_hex
import bcrypt


class User:
    def __init__(
        self,
        name: str,
        password: str,
        email_address: str,
        id: Optional[UUID] = None,
        hash_password: bool = True,
    ) -> None:
        self.id = uuid4() if id is None else id
        self.name = name
        self.password = (
            bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            if hash_password
            else password
        )
        self.email_address = email_address

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, User):
            return self.id == __o.id

        raise NotImplementedError()

    def verify(self, pw: str) -> bool:
        return bcrypt.checkpw(pw.encode(), self.password)

    def generate_token(self) -> None:
        self.token = token_hex()

    def to_dict(self, hide_sensitive_information: bool = True) -> dict:
        data = {
            "name": self.name,
            "id": self.id,
            "email_address": self.email_address,
        }

        if not hide_sensitive_information:
            data["password"] = self.password

        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data["name"], data["password"], data["email_address"], data["id"], False
        )
