from typing import TypeVar, List, Union

T = TypeVar('T')


def di_search(A: List[T], value: T) -> Union[None, int]:
    l = 0
    r = len(A) - 1

    while r >= 1:
        m = (l + r) / 2
        if A[m] == value:
            return m

        if A[m] > value:
            r = m - 1
        else:  # A[m] < value
            l = m + 1

    return None
