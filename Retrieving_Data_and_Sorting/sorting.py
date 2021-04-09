from typing import TypeVar, List, Union, Optional, Callable
from random import random
from sys import stdout
from timeit import timeit
import sys

sys.path.append('../')
from Heap.binheap import binheap

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


def select_pivot(A: List[T], begin: int, end: int, total_order) -> int:
    if end - begin < 5:
        insertion_sort(A, begin=begin, end=end, total_order=total_order)

        return (begin + end) // 2

    c_begin = begin
    pos = begin
    while c_begin + 2 < end + 1:
        insertion_sort(A, begin=c_begin, end=min(end, c_begin + 4), total_order=total_order)

        A[pos], A[c_begin+2] = A[c_begin+2], A[pos]

        pos += 1
        c_begin += 5

    return select(A, (begin+pos-1)//2, begin=begin, end=pos-1, total_order=total_order)


def select(A: List[T], i: int, begin: int = 0, end: Optional[int] = None,
           total_order: Optional[TOrderType] = min_order) -> int:
    if end is None:
        end = len(A) - 1

    if end - begin < 140:
        insertion_sort(A, begin=begin, end=end, total_order=total_order)

        return i

    pivot = select_pivot(A, begin, end, total_order)
    pivot = partition(A, begin, end, pivot, total_order=total_order)

    if i == pivot:
        return i

    if i > pivot:
        return select(A, i, begin=pivot + 1, end=end, total_order=total_order)

    return select(A, i, begin=begin, end=pivot - 1, total_order=total_order)


def quicksort(A: List[T], begin: Optional[int] = 0, end: Optional[int] = None,
              total_order: Optional[TOrderType] = min_order) -> None:
    if end is None:
        end = len(A) - 1

    while begin < end:
        pivot = partition(A, begin, end, begin, total_order=total_order)

        quicksort(A, begin, pivot - 1)
        # quicksort(A, pivot + 1, end) if done with recursion

        begin = pivot + 1


def bubble_sort(A: List[T], begin: Optional[int] = 0, end: Optional[int] = None,
                total_order: Optional[TOrderType] = min_order) -> None:
    if end is None:
        end = len(A) - 1

    for i in range(end, begin, -1):
        for j in range(begin, i):
            if not total_order(A[j], A[j + 1]):
                A[j], A[j + 1] = A[j + 1], A[j]


def reversed_order(total_order: TOrderType) -> TOrderType:
    return lambda a, b: total_order(b, a)


def heapsort(A: List[T], total_order: Optional[TOrderType] = min_order) -> None:
    H = binheap(A, total_order=reversed_order(total_order))  # build a max heap

    for i in range(len(A) - 1, 0, -1):
        A[i] = H.remove_minimum  # extract the maximum from the heap


def counting_sort(A: List[T]) -> List[T]:
    # A[i] in [Min, Max]

    # allocate and initialize C
    C = [0] * (max(A) + 1)

    # count the number of repetitions of each value in A
    for value in A:
        C[value] += 1

    # evaluate the number of values in A <= j
    for j in range(1, len(C)):
        C[j] += C[j - 1]

    # build the resulting array
    B = [None] * len(A)

    # reverse all the A's values in B
    for value in reversed(A):
        B[C[value] - 1] = value
        C[value] -= 1

    return B


def bucket_sort(A: List[T]) -> List[T]:
    # assuming uniform distribution in [0,1)
    # for the values in A

    buckets = [[] for i in range(len(A))]

    for value in A:
        buckets[int(value * len(A))].append(value)

    for j in range(len(buckets)):
        insertion_sort(buckets[j])

    i = 0
    for bucket in buckets:
        for value in bucket:
            A[i] = value
            i += 1


def build_dataset(num_of_arrays: int, size: int) -> List[List[float]]:
    dataset = [None] * num_of_arrays
    for i in range(num_of_arrays):
        dataset[i] = [random() for i in range(size)]

    return dataset


def sort_dataset(dataset, alg):
    for A in dataset:
        alg(A)


if __name__ == '__main__':

    algorithms = ['insertion_sort', 'quicksort', 'bubble_sort', 'heapsort', 'counting_sort', 'bucket_sort']
    dateset_size = 10 ** 4
    # Print the header
    stdout.write('Size')
    for alg in algorithms:
        stdout.write(f'\t{alg}')

    # for all size in [100, 200, ..., 1000]
    for size in range(100, 1100, 100):
        dataset = build_dataset(dateset_size, size)

        stdout.write(f'\n{size}')
        for alg in algorithms:
            dateset_copy = [[value for value in A] for A in dataset]

            T = timeit(f'sort_dataset(dateset_copy, {alg})', globals=locals(), number=1)

            stdout.write(f'\t{T / dateset_size}')
            stdout.flush()

        stdout.write('\n')
