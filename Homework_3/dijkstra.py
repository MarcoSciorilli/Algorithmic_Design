import math
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

def dijkstra_direct(G: Generic, s) -> Generic:
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

def dijkstra_inverse(G: Generic, s) -> Generic:
    A = G.copy()
    init_sssp(A)
    A.get_node(s).set_distance(0)
    Q = build_queue_dijkstra(A)
    while len(Q) != 0:
        u = Q.remove_minimum()
        pointing_nodes = [v for v in A if u in v.adjacent_dict]
        for v in pointing_nodes:
            if v.importance < u.importance:
                continue
            else:
                relax(Q, u, v, v.edge_weight(u))
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

def contraction_hierarchies_list_memory(G: Generic):
    B = G.copy()
    Q = build_queue_hierarchies(G)
    hierarchies =[G]
    i = 1
    while len(Q) != 1:
        u = Q.remove_minimum()
        index = u.index
        u.hierarchy = i
        print(index)
        i += 1
        C = B.copy()
        C.just_node(index)
        hierarchies.append(C)
        B.remove_node(index)
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
                if i.get_node(j.index).edge_weight(i.get_node(t)) < A.get_node(j.index).edge_weight(A.get_node(t)):
                    A.add_edge(j.index, t, j.edge_weight(i.get_node(t)))
    return A

def get_intersection(G, s, e):
    Start = dijkstra_direct(G, s)
    Finish = dijkstra_inverse(G, e)
    connection_distance = math.inf
    connection_index = 0
    for i in Start:
        if i.dijkstra_distance != None and Finish.get_node(i.index).dijkstra_distance != None and (i.dijkstra_distance + Finish.get_node(i.index).dijkstra_distance <connection_distance):
            connection_distance = i.dijkstra_distance + Finish.get_node(i.index).dijkstra_distance
            connection_index = i.index
    return connection_index, connection_distance

def routing(G, s, e):
    Start = dijkstra_direct(G, s)
    Finish = dijkstra_inverse(G, e)
    connection_distance = math.inf
    connection_index = 0
    for i in Start:
        if i.dijkstra_distance != None and Finish.get_node(i.index).dijkstra_distance != None and (i.dijkstra_distance + Finish.get_node(i.index).dijkstra_distance <connection_distance):
            connection_distance = i.dijkstra_distance + Finish.get_node(i.index).dijkstra_distance
            connection_index = i.index
    x = connection_index
    path =[x]
    while Start.get_node(x).dijkstra_pred != None:
        path.append(Start.get_node(x).dijkstra_pred.index)
        x = Start.get_node(x).dijkstra_pred.index
    path. reverse()
    x = connection_index
    while Finish.get_node(x).dijkstra_pred != None:
        path.append(Finish.get_node(x).dijkstra_pred.index)
        x = Finish.get_node(x).dijkstra_pred.index
    return path

def hierarchies_plotter(list_hierarchies, display='file'):
    if len(list_hierarchies) < 2:
        raise RuntimeError('Input has to be a contraction hierarchies')
    vertexes = {}
    keys = list(list_hierarchies[0].graph.keys())
    nodes_number = len(keys)
    for i in range(nodes_number):
        vertexes[keys[i]] = (nodes_number * math.cos(2 * math.pi * i / nodes_number), nodes_number * math.sin(2 * math.pi * i / nodes_number))
    preamble = "\\RequirePackage{luatex85}\n" \
               "\\documentclass{article} \n" \
               "\\usepackage[paperwidth=3000mm, paperheight=3000mm,margin=0mm]{geometry} \n" \
               "\\usepackage{tkz-graph}\n" \
               "\\begin{document}\n"

    starting = "\\begin{figure}\n " \
               "\\centering \n" \
               "\\resizebox{!} {2800mm} { \n" \
               "\\begin{tikzpicture} \n " \
               "\\tikzstyle{EdgeStyle}=[pre] \n"

    ending = "\\end{tikzpicture}} \n" \
             "\\end{figure} \n" \
            "\\newpage \n"
    text = str()
    for g in list_hierarchies:
        text = text + starting
        nodes_list = list(g.graph.keys())
        nodes = str()
        edges = str()
        for i in nodes_list:
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]}] { { i } }\n"
            connections = g.graph[i].get_connections_indexes()
            for j in connections:
                if j == i:
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=${g.graph[i].edge_weight(g.graph[j])}$]({i}) \n"
                else:
                    edges = edges + f"\\Edge[label=${g.graph[i].edge_weight(g.graph[j])}$]({j})({i}) \n"
        for l in keys:
            if l not in nodes_list:
                nodes = nodes + f"\\Vertex[empty, x={vertexes[l][0]},y={vertexes[l][1]}] { {l} }\n"
        text = text + nodes + edges + ending

    preview(text, output='pdf', viewer=display, filename=f'contraction_hierarchies.pdf', euler=False, preamble=preamble)

def vertex_coord(nodes_number):
    return [(nodes_number * math.cos(2 * math.pi * i / nodes_number),
                 nodes_number * math.sin(2 * math.pi * i / nodes_number)) for i in range(nodes_number)]

def plotter_path(G, path, name="graph", display='file'):
    nodes_list = list(G.graph.keys())
    vertexes = vertex_coord(len(nodes_list))
    preamble = "\\RequirePackage{luatex85}\n" \
               "\\documentclass{article} \n" \
               "\\usepackage[paperwidth=5700mm, paperheight=5700mm, margin=0mm]{geometry} \n" \
               "\\usepackage{tkz-graph}\n" \
               "\\begin{document}\n" \
               "\\thispagestyle{empty}"
    starting = "\\begin{figure}\n " \
               "\\centering \n" \
               "\\resizebox{4000mm}{!}{\n" \
               "\\begin{tikzpicture} \n " \
               "\\tikzstyle{EdgeStyle}=[pre] \n"

    nodes = str()
    edges = str()
    for i in range(len(nodes_list)):  # For all the node in the graph
        nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]}] { {nodes_list[i]} } \n"  # Add the nodes
        connections = G.graph[nodes_list[i]].get_connections_indexes()  # For all nodes, make a list of the edges
        for j in connections:  # For all the ending node of the edges of th node studied at the moment
            if j == nodes_list[i]:  # If the node end where it starts, make a loop
                edges = edges + f"\\Loop[dir=NO,dist=2cm,label=${G.graph[nodes_list[i]].edge_weight(G.graph[j])}$]({nodes_list[i]}) \n"
            else:
                if nodes_list[i] in path and j in path:  # If the starting and ending node are both in path (they are surely subsiquent)
                    edges = edges + f"\\Edge[label=${G.graph[nodes_list[i]].edge_weight(G.graph[j])}$, color=red]({j})({nodes_list[i]}) \n"
                    path.remove(nodes_list[i])
                else:
                    edges = edges + f"\\Edge[label=${G.graph[nodes_list[i]].edge_weight(G.graph[j])}$]({j})({nodes_list[i]}) \n"

    ending ="\\end{tikzpicture}} \n" \
            "\\end{figure}"
    formula = starting + nodes + edges + ending
    preview(formula, output='pdf', viewer=display, filename=f'{name}.pdf', euler=False, preamble=preamble)



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

    F = contraction_hierarchies_graph(A)
    path = routing(F, 5, 17)
    plotter_path(F, path)






