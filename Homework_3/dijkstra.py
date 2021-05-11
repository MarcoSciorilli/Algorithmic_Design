from typing import TypeVar, Generic, List, Union
from graph import Graph, Node
from math import inf
import sys

sys.path.append('../')
from Heap.binheap import binheap


def min_dist_order(a: Generic, b: Generic) -> bool:
    return a.dijkstra_distance <= b.dijkstra_distance


def build_queue(G: Generic):
    Q = binheap(A=[v for v in G], total_order=min_dist_order)
    return Q


T = TypeVar('T')


def init_sssp(G: Generic) -> None:
    for v in G:
        v.set_distance(math.inf)


def update_distance(Q, v, d):
    v.dijkstra_distance = d
    if d < math.inf:
        Q.decreaser(Q.get_node(v))
    else:
        Q._heapify(Q.get_node(v))


def relax(Q, u, v, w):
    if u.dijkstra_distance + w < v.dijkstra_distance:
        update_distance(Q, v, u.dijkstra_distance + w)
        v.dijkstra_pred = u


def dijkstra(G: Generic, s) -> Generic:
    init_sssp(A)
    G.get_node(s).set_distance(0)
    Q = build_queue(G)
    while len(Q) != 0:
        u = Q.remove_minimum()
        for v in u.adjacent_dict:
            relax(Q, u, v, u.edge_weight(v))
    return G


if __name__ == '__main__':
    from graph import *

    A = Graph()
    for i in range(20):
        A.add_node(i)
    for i in range(19):
        A.add_edge(i, i + 1, i * 10)
    for i in range(18):
        A.add_edge(i, i + 2, i * 10)
    for i in range(18):
        A.add_edge(2, i + 2, i * 10)
    for i in range(18):
        A.add_edge(6, i + 2, i * 10)
    A.show_graph()
    G = dijkstra(A, 0)
    G.show_dijkstra()
    G.show_path(13)
