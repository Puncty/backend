from typing import Callable, Optional, TypeVar


T = TypeVar("T")


def get_first_match(predicate: Callable[[T], bool], items: list[T]) -> Optional[T]:
    for item in items:
        if predicate(item):
            return item

    return None
