from typing import VarType, Generic, List, Union
from numbers import Number

T = VarType('T')


def min_order(a: Number, b: Number) -> bool:
    return a <= b


def max_order(a: Number, b: Number) -> bool:
    return a >= b


class binheap(Generic[T]):
    LEFT = 0
    RIGHT = 1

    def __init__(self, A: Union[int, List[T]], total_order=None):

        self._torder = total_order
        self._size = 0
        self._A = []
        ...

    @staticmethod
    def parent(self, node: int) -> Union[int, None]:
        if node == 0:
            return None

        return (node - 1) // 2

    @staticmethod
    def child(self, node: int, side: int) -> int:
        return 2 * node + 1 + side

    @staticmethod
    def right(node: int) -> int:
        return 2*node + 2

    def __len__(self):
        return self._size

    def _swap_keys(self, node_a: int, node_b: int) -> None:
        tmp = self._A[node_a]
        self._A[node_a] = self._A[node_b]
        self._A[node_b] = tmp

    def _heapify(self, node: int) -> None:
        keep_fixing = True

        while keep_fixing:
            min_node = node
            for child_idx in [left(node), right(node)]:
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
            raise RuntimeErro('The heap is empty')
        self._swap_keys(0, self._size-1)

        # self._A[0] = self._A[self._size-1]

        self._size = self._size - 1

        return self._A[self._size]

