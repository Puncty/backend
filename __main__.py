from uuid import UUID
from flask import Flask, request

from src.user import User
from src.usercollection import UserCollection

app = Flask(__name__)

uc = UserCollection()


@app.get("/")
def default() -> str:
    return "ok"


@app.post("/register")
def register() -> str:
    user = User(request.form.get("name"),
                request.form.get("password", type=UUID))
    user.generate_token()
    uc.append(user)

    return user.token


if __name__ == "__main__":
    app.run("localhost", "3000")
