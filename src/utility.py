from flask import Request

from src.usercollection import UserCollection


def user_verified(r: Request, uc: UserCollection):
    return uc.by_id(r.form.get("id")).token == r.form.get("token")
