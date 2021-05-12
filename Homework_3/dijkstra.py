from typing import TypeVar, Generic, List, Union
from graph import Graph, Node
from math import inf
import sys

sys.path.append('../')
from Heap.binheap import binheap


def min_dist_order(a: Generic, b: Generic) -> bool:
    return a.dijkstra_distance <= b.dijkstra_distance

def min_import_order(a: Generic, b: Generic) -> bool:
    return a.importance <= b.importance


def build_queue_dijkstra(G: Generic):
    Q = binheap(A=[v for v in G], total_order=min_dist_order)
    return Q

def build_queue_hierarchies(G: Generic):
    Q = binheap(A=[v for v in G], total_order=min_import_order)
    return Q


T = TypeVar('T')


def init_sssp(G: Generic) -> None:
    for v in G:
        v.set_distance(math.inf)
        v.set_pred(None)


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
    Q = build_queue_dijkstra(G)
    while len(Q) != 0:
        u = Q.remove_minimum()
        for v in u.adjacent_dict:
            relax(Q, u, v, u.edge_weight(v))
    return G

def contraction_hierarchies(G: Generic):
    Q = build_queue_hierarchies(G)
    B = G.copy()
    hierarchies =[B]
    i = 0
    while len(Q) != 2:
        u = Q.remove_minimum()
        u.hierarchy = i
        i += 1
        G.remove_node(u.index)
        B = G.copy()
        hierarchies.append(B)
    return hierarchies


def routing(ch: List, s, e):
    G_up = ch[s.index]
    G_down



if __name__ == '__main__':
    from graph import *
    from random import random

    A = Graph()
    for i in range(20):
        A.add_node(i)
        A.get_node(i).importance = random()
    for i in range(19):
        A.add_edge(i, i + 1, i * 10)
    for i in range(18):
        A.add_edge(i, i + 2, i * 10)
    for i in range(18):
        A.add_edge(2, i + 2, i * 10)
    for i in range(18):
        A.add_edge(6, i + 2, i * 10)
    C = dijkstra(A, 0)
    B = contraction_hierarchies(A)

    A.hierarchies_plotter(B)


