import re

EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9\.\-\_\#\!\%\$\'\&\+\*\/\=\?\^\`\{\|\}\~]+@[a-zA-Z0-9\.\-\_]+\.[a-zA-Z0-9\-\_\.]+$")


def is_email(string: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(string))
