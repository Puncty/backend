from typing import Callable, Literal
from flask import Request, request

from src.user import User
from src.usercollection import UserCollection
from src.globals import user_collection


def user_verified(r: Request, uc: UserCollection) -> User | Literal[False]:
    """
    whether or not a user is verified

    :returns: the user when they are verified and False if not
    """
    auth_uname, auth_token = r.authorization.username, r.authorization.password

    user = uc.by_id(auth_uname)
    if user is None:
        user = uc.by_email_address(auth_uname)
        if user is None:
            return False

    if user.token == auth_token:
        return user
    else:
        return False


def require_user_auth(callback: Callable) -> Callable:
    def inner(**kwargs):
        if not (user := user_verified(request, user_collection)):
            return ("Unauthorized", 401)

        return callback(user, **kwargs)

    inner.__name__ = callback.__name__
    return inner


def form_has_values(r: Request, values: list[str]) -> bool:
    for v in values:
        if r.form.get(v) is None:
            return False

    return True
