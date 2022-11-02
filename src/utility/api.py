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
    def wrapper(**kwargs):
        if not (user := user_verified(request, user_collection)):
            return ("Unauthorized", 401)

        return callback(user, **kwargs)

    wrapper.__name__ = callback.__name__
    return wrapper

def require_form_entries(*required_keys: list[str]) -> Callable:
    def inner(callback: Callable):
        def wrapper(**kwargs):
            values = []
            for key in required_keys:
                if not (key in request.form):
                    return ("Invalid form data", 400)
                else:
                    values.append(request.form[key])

            return callback(*values, **kwargs)

        wrapper.__name__ = callback.__name__
        return wrapper
    return inner


def form_has_values(r: Request, values: list[str]) -> bool:
    for v in values:
        if r.form.get(v) is None:
            return False

    return True
