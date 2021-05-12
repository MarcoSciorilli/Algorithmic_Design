from numbers import Number
from typing import TypeVar, Generic, List, Union
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
            # min_node is the index of the minimum key among the keys of root and its children
            if min_node != node:
                self._swap_keys(min_node, node)
                node = min_node
            else:
                keep_fixing = False

    def get_node(self, node: T) -> int:
        for i in range(len(self._A)):
            if self._A[i] == node:
                return i
            else:
                continue

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

    def decrease_key(self, node: int, new_value: T) -> None:
        if self._torder(self._A[node], new_value):
            raise RuntimeError(f'{new_value} is not smaller than' + f'{self._A[node]}')

        self._A[node] = new_value
        self.decreaser(node)

    def decreaser(self, node: int) -> None:
        parent = binheap.parent(node)

        while node != 0 and not self._torder(self._A[parent], self._A[node]):
            self._swap_keys(node, parent)

            node = parent
            parent = binheap.parent(node)

    def insert(self, value: T) -> None:
        if self._size >= len(self._A):
            raise RuntimeError('The heap is full')

        if self.is_empty():
            self._A[0] = value
            self._size += 1
        else:
            parent = binheap.parent(self._size)
            if self._torder(self._A[parent], value):
                self._A[self._size] = value
                self._size += 1
            else:
                self._A[self._size] = self._A[parent]
                self._size += 1
                self.decrease_key(self._size-1, value)

    def __repr__(self) -> str:
        bh_str = ''

        next_node = 1
        up_to = 2

        while next_node <= self._size:
            level = '\t'.join(f'{v}' for v in self._A[next_node - 1: min(up_to - 1, self._size)])

            if next_node == 1:
                bh_str = level
            else:
                bh_str += f'\n{level}'

            next_node = up_to
            up_to = 2 * up_to

        return bh_str

