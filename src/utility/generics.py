from typing import Callable, Optional, TypeVar

T = TypeVar("T")


def get_first_match(predicate: Callable[[T], bool], items: list[T]) -> Optional[T]:
    for item in items:
        if predicate(item):
            return item

    return None

def get_all_matches(predicate: Callable[[T], bool], items: list[T]) -> list[T]:
    matches = []
    
    for item in items:
        if predicate(item):
            matches.append(item)

    return matches
