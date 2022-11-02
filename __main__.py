from datetime import datetime
from typing import Optional
from uuid import UUID
from flask import Flask, request
from src.meetup import Meetup
from src.meetupcollection import MeetupCollection

from src.user import User
from src.utility.api import form_has_values, user_verified
from src.usercollection import UserCollection

app = Flask(__name__)

uc = UserCollection()
mc = MeetupCollection()


RETURN_UNAUTHORIZED = ("Unauthorized", 401)


@app.get("/")
def default() -> str:
    return "ok"


@app.post("/account/register")
def register() -> str | tuple:
    if not form_has_values(request, ["name", "password", "email-address"]):
        return ("Invalid form data", 400)

    if not (uc.by_email_address(request.form.get("email-address")) is None):
        return ("Email already in use", 400)

    user = User(request.form.get("name"),
                request.form.get("password"),
                request.form.get("email-address"))
    user.generate_token()
    uc.append(user)

    return {
        "id": user.id,
        "token": user.token
    }


@app.post("/account/login")
def login() -> str | tuple:
    user = uc.by_id(UUID(request.form.get("email-address")))
    if not (user is None) and user.verify(request.form.get("password")):
        user.generate_token()
        return {
            "id": user.id,
            "token": user.token
        }
    else:
        return RETURN_UNAUTHORIZED


@app.delete("/account")
def delete_account() -> str | tuple:
    if not user_verified(request, uc):
        return RETURN_UNAUTHORIZED

    user = uc.by_id(request.form.get("user-id"))
    uc.remove(user)

    return "ok"


@app.post("/meetup/create")
def create_meetup() -> str | tuple:
    if not user_verified(request, uc):
        return RETURN_UNAUTHORIZED

    if not form_has_values(request, ["user-id", "datetime", "location"]):
        return ("Bad Request", 400)

    user = uc.by_id(request.form.get("user-id"))
    timestamp = request.form.get("datetime", type=int)
    location = request.form.get("location")
    meetup = Meetup(user, datetime.fromtimestamp(timestamp), location)
    mc.append(meetup)

    return meetup.id.hex


@app.put("/meetup/<meetup_id>/join")
def join_meetup(meetup_id: str) -> str:
    if not user_verified(request, uc):
        return RETURN_UNAUTHORIZED

    user = uc.by_id(request.form.get("user-id"))

    meetup = mc.by_id(meetup_id)
    meetup.join(user)

    return meetup.to_dict()


@app.delete("/meetup/<meetup_id>")
def delete_meetup(meetup_id: str) -> Optional[tuple]:
    user = uc.by_id(request.form.get("user-id"))
    meetup = mc.by_id(meetup_id)
    if not user_verified(request, uc) or user != meetup.admin:
        return RETURN_UNAUTHORIZED

    mc.remove(meetup)

    return "ok"


if __name__ == "__main__":
    app.run("localhost", "3000")
