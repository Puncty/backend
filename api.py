from datetime import datetime
from typing import Optional
from flask import Flask
from src.meetup import Meetup

from src.user import User
from src.utility.api import require_user_auth, require_form_entries
from src.globals import user_collection as uc, meet_collection as mc

app = Flask(__name__)


@app.get("/")
def default() -> str:
    return "ok"


@app.post("/account/register")
@require_form_entries("name", "password", "email-address")
def register(name: str, password: str, email_address: str) -> str | tuple:
    if not (uc.by_email_address(email_address) is None):
        return "Email already in use", 400

    user = User(name, password, email_address)
    user.generate_token()
    uc.append(user)

    return {"id": user.id, "token": user.token}


@app.post("/account/login")
@require_form_entries("email-address", "password")
def login(email_address: str, password: str) -> str | tuple:
    user = uc.by_email_address(email_address)
    if not (user is None) and user.verify(password):
        user.generate_token()
        return {"id": user.id, "token": user.token}
    else:
        return "Wrong Credentials", 401


@app.delete("/account")
@require_user_auth
def delete_account(user: User) -> str | tuple:
    uc.remove(user)

    return "ok"


@app.post("/meetup/create")
@require_form_entries("datetime", "location")
@require_user_auth
def create_meetup(user: User, timestamp: int, location: str, _) -> str | tuple:
    meetup = Meetup(user, datetime.fromtimestamp(timestamp), location)
    mc.append(meetup)

    return meetup.id.hex


@app.get("/meetup/<meetup_id>")
@require_user_auth
def get_meetup(user: User, meetup_id: str) -> str:
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
    meetup = mc.by_id(meetup_id)
    meetup.join(user)

    return meetup.to_dict()


@app.put("/meetup/<meetup_id>/leave")
@require_user_auth
def leave_meetup(user: User, meetup_id: str) -> str:
    meetup = mc.by_id(meetup_id)
    if meetup is None:
        return f"The meetup id {meetup_id} does not exist", 404

    meetup.leave(user)

    return "ok"


@app.delete("/meetup/<meetup_id>")
@require_user_auth
def delete_meetup(user: User, meetup_id: str) -> Optional[tuple]:
    meetup = mc.by_id(meetup_id)
    if user != meetup.admin:
        return "You are not the admin of the meeting", 401

    mc.remove(meetup)

    return "ok"


if __name__ == "__main__":
    app.run("localhost", "3000")
