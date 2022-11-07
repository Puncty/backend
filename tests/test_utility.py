import setup_test
from src.utility.general import is_email
from src.utility.generics import get_first_match, get_all_matches


def test_email_verification():
    assert is_email("test@example.com")
    assert not is_email("This is not an @ email")
    assert not is_email("@server.de")
    assert not is_email("me@server")
    assert is_email("me@server.de")


def test_get_first_match():
    assert get_first_match(lambda x: x[0] == "T", [
                           "Test", "best", "Nest"]) == "Test"
    assert get_first_match(lambda x: x.endswith("est") or x[0] == "T", [
                           "Nest", "Test", "best"]) == "Nest"


def test_get_all_matches():
    pool = ["Hello", "test", "Something"]

    assert get_all_matches(lambda x: x[0].isupper(), pool) == [
        "Hello", "Something"]
    assert get_all_matches(lambda x: x[0].islower(), pool) == [
        "test"]
