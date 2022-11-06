import setup_test
from src.utility.general import is_email


def test_email_verification():
    assert is_email("test@example.com")
    assert not is_email("This is not an @ email")
    assert not is_email("@server.de")
    assert not is_email("me@server")
    assert is_email("me@server.de")
