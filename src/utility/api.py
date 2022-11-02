from flask import Request

from src.usercollection import UserCollection


def user_verified(r: Request, uc: UserCollection, attr_name="user-id"):
    user = uc.by_id(r.form.get(attr_name))
    if user is None:
        return False

    return user.token == r.form.get("token")


def form_has_values(r: Request, values: list[str]) -> bool:
    for v in values:
        if r.form.get(v) is None:
            return False

    return True
