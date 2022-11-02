from datetime import datetime
from typing import Optional
from uuid import UUID
from flask import Flask, request
from src.meetup import Meetup

from src.user import User
from src.utility.api import require_user_auth, require_form_entries
from src.globals import user_collection as uc, meet_collection as mc

app = Flask(__name__)


RETURN_UNAUTHORIZED = ("Unauthorized", 401)
RETURN_FORM_DATA_ERROR = ("Invalid form data", 400)


@app.get("/")
def default() -> str:
    return "ok"


@app.post("/account/register")
@require_form_entries("name", "password", "email-address")
def register(name: str, password: str, email_address: str) -> str | tuple:
    if not (uc.by_email_address(email_address) is None):
        return ("Email already in use", 400)

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
        return RETURN_UNAUTHORIZED


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
        return RETURN_FORM_DATA_ERROR

    if meetup.is_member(user):
        return meetup.to_dict()
    else:
        return RETURN_UNAUTHORIZED


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
        return RETURN_FORM_DATA_ERROR

    meetup.leave(user)

    return "ok"


@app.delete("/meetup/<meetup_id>")
@require_user_auth
def delete_meetup(user: User, meetup_id: str) -> Optional[tuple]:
    meetup = mc.by_id(meetup_id)
    if user != meetup.admin:
        return RETURN_UNAUTHORIZED

    mc.remove(meetup)

    return "ok"


if __name__ == "__main__":
    app.run("localhost", "3000")
