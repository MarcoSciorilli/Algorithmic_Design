from typing import TypeVar, List, Union, Optional, Callable
from random import random
from sys import stdout
from timeit import timeit

T = TypeVar('T')

TOrderType = Callable[[T, T], bool]


def min_order(a: T, b: T) -> bool:
    return a <= b


def di_search(A: List, value: T, total_order: Optional[TOrderType] = None) -> Union[None, int]:
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


def insertion_sort(A: List[T], begin: int = 0, end: Optional[int] = None,
                   total_order: Optional[TOrderType] = None) -> None:
    if total_order is None:
        total_order = min_order

    if end is None:
        end = len(A) - 1

    for i in range(begin + 1, end + 1):
        j = i
        while j > begin and not total_order(A[j - 1], A[j]):  # A[j] < A[j-1] <=> not (A[j-1] <= A[j])
            A[j], A[j - 1] = A[j - 1], A[j]

            j -= 1


def partition(A: List[T], begin: int, end: int, pivot: int, total_order: Optional[TOrderType] = min_order) -> int:
    A[begin], A[pivot] = A[pivot], A[begin]

    pivot = begin
    begin = begin + 1

    while end >= begin:
        if total_order(A[begin], A[pivot]):
            begin += 1
        else:
            A[begin], A[end] = A[end], A[begin]
            end -= 1
    A[pivot], A[end] = A[end], A[pivot]
    return end


def quicksort(A: List[T], begin: Optional[int] = 0, end: Optional[int] = None,
              total_order: Optional[TOrderType] = min_order) -> None:
    if end is None:
        end = len(A) - 1

    while begin < end:
        pivot = partition(A, begin, end, begin, total_order=total_order)

        quicksort(A, begin, pivot - 1)
        # quicksort(A, pivot + 1, end) if done with recursion

        begin = pivot + 1


def build_dataset(num_of_arrays: int, size: int) -> List[List[float]]:
    dataset = [None] * num_of_arrays
    for i in range(num_of_arrays):
        dataset[i] = [random() for i in range(size)]

    return dataset


def sort_dataset(dataset, alg):
    for A in dataset:
        alg(A)


if __name__ == '__main__':

    for size in range(100, 1100, 100):
        dataset = build_dataset(100, size)

        T = timeit(f'sort_dataset(dataset, insertion_sort)', globals=locals(), number=1)

        stdout.write(f'{size}\t{T}\n')
        stdout.flush()
