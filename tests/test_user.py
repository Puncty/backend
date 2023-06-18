import setup_test
from uuid import UUID
from src.user import User


def test_create_user():
    u = User("Test", "1234", "example@server.com")

    assert u.password != "1234"
    assert isinstance(u.id, UUID)

    u.generate_token()

    assert u.token != None
    assert isinstance(u.token, str)


def test_verifying_user():
    u = User("Test", "1234", "example@server.com")

    assert u.verify("1234")
    assert not u.verify("5678")


def test_serialization():
    u = User("Test", "1234", "example@server.com")
    serialized = u.to_dict(False)

    assert isinstance(serialized, dict)
    assert User.from_dict(serialized) == u
