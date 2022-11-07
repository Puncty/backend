from datetime import datetime

import setup_test
from src.user import User
from src.meetup import Meetup
from src.usercollection import UserCollection


def test_create_meetup():
    admin = User("Test", "1234", "example@server.com")
    m = Meetup(admin, datetime.now(), "abc")

    assert m.admin == admin
    assert m.is_member(admin)


def test_members_in_meetup():
    admin = User("Admin", "1234", "example@server.com")
    u1 = User("User1", "1234", "example2@server.com")
    m = Meetup(admin, datetime.now(), "somewhere")

    assert m.is_member(admin)
    assert not m.is_member(u1)
    m.join(u1)
    assert m.is_member(u1)
    m.leave(u1)
    assert not m.is_member(u1)


def test_meetup_serialization():
    uc = UserCollection()
    admin = User("Admin", "1234", "example@server.com")
    uc.append(admin)
    m1 = Meetup(admin, datetime.now(), "somewhere")
    m2 = Meetup(admin, datetime.now(), "somewhere else")

    assert m1.to_dict() != m2.to_dict()
    assert Meetup.from_dict(m1.to_dict(), uc) == m1
