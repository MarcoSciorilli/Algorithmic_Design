from typing import TypeVar, Any, Union, Optional
from collections.abc import Callable

T = TypeVar('T')


def min_order(a: T, b: T) -> bool:
    return a <= b


def di_search(A: Any, value: T, total_order = None) -> Union[None, int]:
    l = 0
    r = len(A) - 1

    if total_order is None:
        total_order = min_order

    while r >= 1:
        m = (l + r) // 2
        if total_order(A[m], value):  # A[m].id <= value
            if total_order(value, A[m]):  # A[m] >= value
                return m

            l = m + 1
        else:
            r = m - 1

        if A[m] == value:
            return m

        if A[m] > value:
            r = m - 1
        else:  # A[m] < value
            l = m + 1

    return None
