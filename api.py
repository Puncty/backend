from datetime import datetime
from typing import Optional
from flask import Flask, request, redirect

from src.user import User
from src.meetup import Meetup
from src.usercollection import UserCollection
from src.meetupcollection import MeetupCollection
from src.utility.api import require_user_auth, require_form_entries
from src.utility.general import is_email
from src.utility.storage import Storage

app = Flask(__name__)
storage = Storage("data/data.json")


def mutate_uc(
    uc: UserCollection): storage["user-collection"] = uc.to_dict(False)


def mutate_mc(
    mc: MeetupCollection): storage["meetup-collection"] = mc.to_dict(False, True)


uc = UserCollection.load(storage, on_mutation=mutate_uc)
mc = MeetupCollection.load(storage, uc, on_mutation=mutate_mc)


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
    if not is_email(email_address):
        return "Invalid email address", 400

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
@require_user_auth(uc)
def delete_account(user: User) -> str | tuple:
    """
    delete a user's account

    :param user: the user to delete
    """
    uc.remove(user)

    return "ok"


@app.get("/user/me")
@require_user_auth(uc)
def get_me(me: User) -> dict:
    """
    get information about the logged in user

    :param me: the logged in user
    """
    return me.to_dict()


@app.get("/user/<user_id>")
@require_user_auth(uc)
def get_user(_, user_id: str) -> dict:
    """
    get information about a certain user

    :param user_id: the id of the user to get information about
    """
    user = uc.by_id(user_id)
    if user is None:
        return "User not found", 404

    return user.to_dict()


@app.post("/meetup")
@require_form_entries("datetime", "location")
@require_user_auth(uc)
def create_meetup(user: User, timestamp: str, location: str) -> str | tuple:
    """
    create a new meetup

    :param user: the user which wants create the meetup
    :param timestamp: the date/time when the meetup should take place, in the unix time format
    :param location: the location where the meetup should take place, in a google maps compatible format
    """
    meetup = Meetup(user, datetime.fromtimestamp(int(timestamp)), location)
    if meetup.datetime < datetime.now():
        return "Meetup can not be set in past", 400
    else:
        mc.append(meetup)
        return meetup.id.hex


@app.get("/meetup")
@require_user_auth(uc)
def get_users_meetups(user: User) -> list[str]:
    """
    get the meetups in which the user is a member

    :param user: the user which is supposed to appear as a member in the meetups
    """
    return {"meetups": list(map(lambda x: str(x.id), mc.with_member(user)))}


@app.get("/meetup/<meetup_id>")
@require_user_auth(uc)
def get_meetup(user: User, meetup_id: str) -> str:
    """
    get information about a certain meetup, if the user is a member of it

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


@app.get("/meetup/<meetup_id>/join")
def join_meetup_in_app(meetup_id: str) -> str:
    return redirect(f"puncty://join/{meetup_id}", code=302)


@app.put("/meetup/<meetup_id>/join")
@require_user_auth(uc)
def join_meetup(user: User, meetup_id: str) -> str:
    """
    join a certain meetup

    :param user: the user that wants to join the meetup
    :param meetup_id: the id of the meetup to join
    """
    meetup = mc.by_id(meetup_id)
    if meetup is None:
        return f"The meetup id {meetup_id} does not exist", 404

    meetup.join(user)

    return meetup.to_dict()


@app.put("/meetup/<meetup_id>/leave")
@require_user_auth(uc)
def leave_meetup(user: User, meetup_id: str) -> str:
    """
    leave a certain meetup

    :param user: the user that wants to leave
    :param meetup_id: the id of the meetup to leave
    """
    meetup = mc.by_id(meetup_id)
    if meetup is None:
        return f"The meetup id {meetup_id} does not exist", 404

    meetup.leave(user)

    return "ok"


@app.patch("/meetup/<meetup_id>")
@require_user_auth(uc)
def edit_meetup(user: User, meetup_id: str) -> tuple | dict:
    """
    edit the properties of a certain meetup

    :param user: the user to edit the meetup, which has to be it's admin
    :param meetup_id: the id of the meetup to edit
    """
    meetup = mc.by_id(meetup_id)
    if meetup is None:
        return f"The meetup id {meetup_id} does not exist", 404

    if user != meetup.admin:
        return "You are not the admin of the meeting", 401

    meetup.datetime = request.form["datetime"] if "datetime" in request.form else meetup.datetime
    meetup.location = request.form["location"] if "location" in request.form else meetup.location

    new_admin_id = request.form["admin"] if "admin" in request.form else None
    if new_admin_id and (new_admin := uc.by_id(new_admin_id)) and meetup.is_member(new_admin):
        meetup.admin = new_admin

    return meetup.to_dict()


@app.delete("/meetup/<meetup_id>")
@require_user_auth(uc)
def delete_meetup(user: User, meetup_id: str) -> Optional[tuple]:
    """
    delete a certain meetup if the user is the admin of it

    :param user: the user, which has to be the admin of the meetup
    :param meetup_id: the id of the meetup to delete
    """
    meetup = mc.by_id(meetup_id)
    if meetup is None:
        return f"The meetup id {meetup_id} does not exist", 404

    if user != meetup.admin:
        return "You are not the admin of the meeting", 401

    mc.remove(meetup)

    return "ok"


if __name__ == "__main__":
    app.run("localhost", "8002")
