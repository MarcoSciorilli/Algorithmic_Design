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
    i = 0
    A = []
    for v in G:
        A.append(v)
        v.binheap_index = i
        i += 1
    Q = binheap(A=A, total_order=min_dist_order)
    return Q

def build_queue_hierarchies(G: Generic):
    i = 0
    A = []
    for v in G:
        A.append(v)
        v.binheap_index = i
        i += 1
    Q = binheap(A=A, total_order=min_import_order)
    return Q


T = TypeVar('T')


def init_sssp(G: Generic) -> None:
    for v in G:
        v.set_distance(math.inf)
        v.set_pred(None)


def update_distance(Q, v, d):
    v.dijkstra_distance = d
    if d < math.inf:
        Q.decreaser(v.binheap_index)
    else:
        Q._heapify(v.binheap_index)


def relax(Q, u, v, w):
    if u.dijkstra_distance + w < v.dijkstra_distance:
        update_distance(Q, v, u.dijkstra_distance + w)
        v.dijkstra_pred = u


def dijkstra(G: Generic, s) -> Generic:
    A = G.copy()
    init_sssp(A)
    A.get_node(s).set_distance(0)
    Q = build_queue_dijkstra(A)
    while len(Q) != 0:
        u = Q.remove_minimum()
        for v in u.adjacent_dict:
            relax(Q, u, v, u.edge_weight(v))
    return A

def dijkstra_higher(G: Generic, s) -> Generic:
    A = G.copy()
    init_sssp(A)
    A.get_node(s).set_distance(0)
    Q = build_queue_dijkstra(A)
    while len(Q) != 0:
        u = Q.remove_minimum()
        for v in u.adjacent_dict:
            if v.importance < u.importance:
                continue
            else:
                relax(Q, u, v, u.edge_weight(v))
    return A

def dijkstra_lower(G: Generic, s) -> Generic:
    A = G.copy()
    init_sssp(A)
    A.get_node(s).set_distance(0)
    Q = build_queue_dijkstra(A)
    while len(Q) != 0:
        u = Q.remove_minimum()
        for v in u.adjacent_dict:
            if v.importance > u.importance:
                continue
            else:
                relax(Q, u, v, u.edge_weight(v))
    return A

def contraction_hierarchies_list(G: Generic):
    B = G.copy()
    First_element = G.copy()
    Q = build_queue_hierarchies(First_element)
    hierarchies =[First_element]
    i = 0
    while len(Q) != 2:
        u = Q.remove_minimum()
        u.hierarchy = i
        i += 1
        B.remove_node(u.index)
        C = B.copy()
        hierarchies.append(C)
    return hierarchies

def contraction_hierarchies_graph(G: Generic):
    A = G.copy()
    hierarchies = contraction_hierarchies_list(A)
    for i in hierarchies:
        for j in i:
            connections = j.get_connections_indexes()
            for t in connections:
                if t not in A.get_node(j.index).get_connections_indexes():
                    A.add_edge(j.index, t, j.edge_weight(i.get_node(t)))
    return A


def routing(G, s, e):
    Start = dijkstra_higher(G, s)
    Finish = dijkstra_lower(G, e)



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
    F = dijkstra(A, 0)
    F.plotter("path")



