from typing import TypeVar, Generic, List, Union
from numbers import Number

T = TypeVar('T')


def min_order(a: Number, b: Number) -> bool:
    return a <= b


def max_order(a: Number, b: Number) -> bool:
    return a >= b


class binheap(Generic[T]):
    LEFT = 0
    RIGHT = 1

    def __init__(self, A: Union[int, List[T]], total_order=None):

        if total_order is None:
            self._torder = min_order
        else:
            self._torder = total_order
        if isinstance(A, int):
            self._size = 0
            self._A = [None] * A
        else:
            self._size = len(A)
            self._A = A

        self._build_heap()

    @staticmethod
    def parent(node: int) -> Union[int, None]:
        if node == 0:
            return None

        return (node - 1) // 2

    @staticmethod
    def child(node: int, side: int) -> int:
        return 2 * node + 1 + side

    @staticmethod
    def left(node: int) -> int:
        return 2 * node + 1

    @staticmethod
    def right(node: int) -> int:
        return 2 * node + 2

    def __len__(self):
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def _swap_keys(self, node_a: int, node_b: int) -> None:
        tmp = self._A[node_a]
        self._A[node_a] = self._A[node_b]
        self._A[node_b] = tmp

    def _heapify(self, node: int) -> None:
        keep_fixing = True

        while keep_fixing:
            min_node = node
            for child_idx in [binheap.left(node), binheap.right(node)]:
                if child_idx < self._size and self._torder(self._A[child_idx], self._A[min_node]):
                    min_node = child_idx
            # min_node is the index of the minimum key among the keys of root and its childrend
            if min_node != node:
                self._swap_keys(min_node, node)
                node = min_node
            else:
                keep_fixing = False

    def remove_minimum(self) -> T:
        if self.is_empty():
            raise RuntimeError('The heap is empty')
        self._swap_keys(0, self._size - 1)

        # self._A[0] = self._A[self._size-1]

        self._size = self._size - 1

        self._heapify(0)

        return self._A[self._size]

    def _build_heap(self) -> None:
        for i in range(self._size - 1, -1, -1):
            self._heapify(i)

    def __repr__(self) -> str:
        bh_str = ''

        next_node = 1
        up_to = 2

        while next_node <= self._size:
            level = '\t'.join(f'{v}' for v in self._A[next_node - 1: up_to - 1])

            if next_node == 1:
                bh_str = level
            else:
                bh_str += f'\n{level}'

            next_node = up_to
            up_to = 2 * up_to

        return bh_str
