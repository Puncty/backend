from datetime import datetime
from flask import Flask, request
from src.meetup import Meetup
from src.meetupcollection import MeetupCollection

from src.user import User
from src.usercollection import UserCollection
from src.utility import user_verified

app = Flask(__name__)

uc = UserCollection()
mc = MeetupCollection()


@app.get("/")
def default() -> str:
    return "ok"


@app.post("/register")
def register() -> str:
    user = User(request.form.get("name"),
                request.form.get("password"))
    user.generate_token()
    uc.append(user)

    return user.token


def login() -> str | tuple:
    user = uc.by_id(request.form.get("id"))
    if user.verify(request.form.get("password")):
        user.generate_token()
        return user.token
    else:
        return ("Unauthorized", 401)


@app.post("/meetup/create")
def create_meetup() -> str | tuple:
    if not user_verified(request, uc):
        return ("Unauthorized", 401)

    timestamp = request.form.get("datetime", type=int)
    location = request.form.get("location")
    meetup = Meetup([], datetime.fromtimestamp(timestamp), location)
    mc.append(meetup)

    return meetup.id


if __name__ == "__main__":
    app.run("localhost", "3000")
