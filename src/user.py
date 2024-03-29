from typing import Optional
from uuid import uuid4, UUID
from secrets import token_hex
import bcrypt


class User:
    def __init__(
        self,
        name: str,
        password: str | bytes,
        email_address: str,
        id: Optional[UUID] = None,
        hash_password: bool = True,
    ) -> None:
        self.id = uuid4() if id is None else UUID(id)
        self.name = name
        self.password = (
            bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            if hash_password
            else password
        )
        self.email_address = email_address.lower()
        self.generate_token()

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, User):
            return self.id == __o.id

        raise NotImplementedError()

    def verify(self, pw: str) -> bool:
        """
        verify that the entered password matches the users password-hash

        :param pw: the password to check
        """
        return bcrypt.checkpw(pw.encode(), self.password)

    def generate_token(self) -> None:
        """
        generate a new auth token
        """
        self.token = token_hex()

    def to_dict(self, hide_sensitive_information: bool = True) -> dict:
        data = {
            "name": self.name,
            "id": str(self.id),
            "email_address": self.email_address,
        }

        if not hide_sensitive_information:
            data["password"] = self.password.decode()

        return data

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data["name"], data["password"].encode(
            ), data["email_address"], data["id"], False
        )
