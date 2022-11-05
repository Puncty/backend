from datetime import datetime
from typing import Optional
from flask import Flask

from src.user import User
from src.meetup import Meetup
from src.utility.api import require_user_auth, require_form_entries
from src.globals import user_collection as uc, meet_collection as mc

app = Flask(__name__)


@app.get("/")
def default() -> str:
    return "ok"


@app.post("/account/register")
@require_form_entries("name", "password", "email-address")
def register(name: str, password: str, email_address: str) -> str | tuple:
    """
    register a new user

    :param name: the name of the registering user
    :param password: the password of the registering user
    :param email_address: the email address of the registering user,
        which should has to be unique to the ones of other registered user:
    """
    if not (uc.by_email_address(email_address) is None):
        return "Email already in use", 400

    user = User(name, password, email_address)
    user.generate_token()
    uc.append(user)

    return {"id": user.id, "token": user.token}


@app.post("/account/login")
@require_form_entries("email-address", "password")
def login(email_address: str, password: str) -> str | tuple:
    """
    log in an already existing user

    :param email_address: the user's email address
    :param password: the (unhashed/plain) password of the user
    """
    user = uc.by_email_address(email_address)
    if not (user is None) and user.verify(password):
        user.generate_token()
        return {"id": user.id, "token": user.token}
    else:
        return "Wrong Credentials", 401


@app.delete("/account")
@require_user_auth
def delete_account(user: User) -> str | tuple:
    """
    delete a user's account

    :param user: the user to delete
    """
    uc.remove(user)

    return "ok"


@app.get("/user/me")
@require_user_auth
def get_me(me: User) -> dict:
    return me.to_dict()


@app.get("/user/<user_id>")
@require_user_auth
def get_user(_, user_id: str) -> dict:
    user = uc.by_id(user_id)
    if user is None:
        return "User not found", 404

    return user.to_dict()


@app.post("/meetup")
@require_form_entries("datetime", "location")
@require_user_auth
def create_meetup(user: User, timestamp: int, location: str, _) -> str | tuple:
    """
    create a new meetup

    :param user: the user which wants create the meetup
    :param timestamp: the date/time when the meetup should take place, in the unix time format
    :param location: the location where the meetup should take place, in a google maps compatible format
    """
    meetup = Meetup(user, datetime.fromtimestamp(timestamp), location)
    mc.append(meetup)

    return meetup.id.hex


@app.get("/meetup")
@require_user_auth
def get_users_meetups(user: User) -> list[str]:
    return list(map(lambda x: str(x.id), mc.with_member(user)))

@app.get("/meetup/<meetup_id>")
@require_user_auth
def get_meetup(user: User, meetup_id: str) -> str:
    """
    get information about a certain meetup, if the user is a member of it.

    :param user: the user that wants to get the information
    :param meetup_id: the id of the meetup
    """
    meetup = mc.by_id(meetup_id)
    if meetup is None:
        return f'The meetup id "{meetup_id}" does not exist', 404

    if meetup.is_member(user):
        return meetup.to_dict()
    else:
        return "You are not a member of this meetup", 401


@app.put("/meetup/<meetup_id>/join")
@require_user_auth
def join_meetup(user: User, meetup_id: str) -> str:
    """
    join a certain meetup.

    :param user: the user that wants to join the meetup
    :param meetup_id: the id of the meetup to join
    """
    meetup = mc.by_id(meetup_id)
    meetup.join(user)

    return meetup.to_dict()


@app.put("/meetup/<meetup_id>/leave")
@require_user_auth
def leave_meetup(user: User, meetup_id: str) -> str:
    """
    leave a certain meetup.

    :param user: the user that wants to leave
    :param meetup_id: the id of the meetup to leave
    """
    meetup = mc.by_id(meetup_id)
    if meetup is None:
        return f"The meetup id {meetup_id} does not exist", 404

    meetup.leave(user)

    return "ok"


@app.delete("/meetup/<meetup_id>")
@require_user_auth
def delete_meetup(user: User, meetup_id: str) -> Optional[tuple]:
    """
    delete a certain meetup if the user is the admin of it.

    :param user: the user, which has to be the admin of the meetup
    :param meetup_id: the id of the meetup to delete
    """

    meetup = mc.by_id(meetup_id)
    if user != meetup.admin:
        return "You are not the admin of the meeting", 401

    mc.remove(meetup)

    return "ok"


if __name__ == "__main__":
    app.run("localhost", "3000")
