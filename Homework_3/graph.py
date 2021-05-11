from typing import TypeVar, KeysView, Optional, List, Generic
from sympy import *
import math

K = TypeVar('K')


class Node:
    """
    Adjacency list representation of a weighted graph node, implemented using a python dictionary
    """

    def __init__(self, vertex: int):
        self.index = vertex
        self.adjacent_dict = {}
        self.dijkstra_distance = None
        self.dijkstra_pred = None
        self.importance = None

    def __str__(self) -> str:
        return str(self.index) + ' adjacent: ' + str([x.index for x in self.adjacent_dict])

    def add_connected_node(self, connected_node: Generic, weight: K = 1) -> None:
        """
        Function which adds a node to the adjacency list of the node,
        with the corresponding weight of the edge

        Parameters
        ----------
        connected_node: index of the connected node
        weight: weight of the edge
        -------

        """
        if weight < 0:
            raise RuntimeError('Weights cannot be negative')

        else:
            self.adjacent_dict[connected_node] = weight

    def get_connections(self) -> KeysView:
        """
        Function which returns the indexes of the connected nodes
        Returns: keys of the adjacency list dictionary

        """
        return self.adjacent_dict.keys()

    def get_connections_indexes(self) -> List:
        """
        Function which returns the indexes of the connected nodes
        Returns: keys of the adjacency list dictionary

        """
        return [x.index for x in self.adjacent_dict]

    def edge_weight(self, connected_node: int) -> bool:
        """
        Function which returns the weight of the edge to a specific node.
        Parameters
        ----------
        connected_node: the connected node whose edge we are interested in

        Returns: the weight of the edge
        -------

        """
        return self.adjacent_dict[connected_node]


    def set_distance(self, d: K) -> None:
        self.dijkstra_distance = d


    def set_pred(self, pred: K) -> None:
        self.dijkstra_pred = pred


    def set_importance(self, importance: K) -> None:
        self.importance = importance



class Graph:
    """
    Adjacency list representation of a weighted graph,implemented using a python dictionary
    """
    def __init__(self):
        self.graph = {}
        self.length_graph = 0

    def __iter__(self):
        return iter(self.graph.values())

    def put_node(self, starting_edges: List[Tuple], ending_edges: List[Tuple]) -> None:
        """
        Function which adds a node to the graph, with all the wanted edges
        Parameters
        ----------
        starting_edges: List of edges starting from the node made of pairs( the aim node and the weight
                        of the edge).
        ending_edges: List of edges ending in the node,  made of pairs (the starting node, and the weight
                        of the edge).
        -------

        """
        index = self. length_graph + 1
        self.add_node(index)
        for x in starting_edges:
            self.graph[index].add_connected_node(self.graph[x[0]], x[1])
        for y in ending_edges:
            self.graph[y[0]].add_connected_node(self.graph[index], y[1])

    def add_node(self, index: int) -> Node:
        """
        Function which add a new node with a given index to the graph
        Parameters
        ----------
        index: index of the new node

        Returns: the node
        -------

        """
        if index in self.graph:
            raise RuntimeError('Node with the same index already present')
        else:
            self.length_graph = self.length_graph + 1  # Increase the length of the graph
            new_node = Node(index)  # Create a node with the given index
            self.graph[index] = new_node  # Put the new node in the graph
            return new_node

    def get_node(self, index: int) -> Optional[Node]:
        """
        Function which returns a node in the graph.
        Parameters
        ----------
        index: index of the node of interest

        Returns: the node of interest
        -------

        """
        if index in self.graph:
            return self.graph[index]
        else:
            raise RuntimeError('Node not in the graph')

    def add_edge(self, start: int, end: int, weight: K = 0) -> None:
        """
        Function which create an edge between two nodes.
        Parameters
        ----------
        start: index of the starting node
        end: index of the ending node
        weight: weight of the edge
        -------

        """

        if start not in self.graph:
            raise RuntimeError('Starting node not in the graph')
        if end not in self.graph:
            raise RuntimeError('Ending node not in the graph')
        self.graph[start].add_connected_node(self.graph[end], weight)

    def get_nodes(self) -> KeysView:
        """
        Function which return a list of all the nodes in the graph
        Returns: list of all the nodes in the graph.
        -------

        """
        return self.graph.keys()

    def get_nodes_list(self) -> list:
        """
        Function which returns a list of the index of all the nodes in the graph
        Returns: list of all the nodes in the graph.
        -------

        """
        return list(self.graph.keys())

    def get_distances(self):
        """
        After an application of the Dijkstra algorithm, the function which returns a list of the distances
        of all nodes from the origin.
        """
        distances = [self.get_node(v).dijkstra_distance for v in self.graph]
        return distances

    def get_pred(self):
        """
        Function which return the list of the precedent node for all the nodes in the graph.
        """
        pred = [self.get_node(v).dijkstra_pred for v in self.graph]
        return pred

    def _get_path(self, end):
        """
        After an application of the Dijkstra algorithm, the function return the node path from the origin
        to the node given in input.
        Parameters
        ----------
        end Aimed node
        -------

        """
        path = [end]
        while end.dijkstra_pred != None:
            path.append(end.dijkstra_pred)
            end = end.dijkstra_pred
        return path

    def remove_node(self, node):
        node = self.get_node(node)
        starting_nodes = [self.get_node(v) for v in self.graph if node in self.get_node(v).adjacent_dict]
        for n in starting_nodes:  # for all the nodes that points to the one to remove
            for m in node.adjacent_dict:  # for all the nodes the one to remove points to
                # if the nodes points at each other, or the
                # there already is a shorter path, skip the iteration
                if m == n or (m in n.adjacent_dict) and (n.edge_weight(m) < n.edge_weight(node) + node.edge_weight(m)):
                    continue
                else:
                    self.add_edge(n.index, m.index, n.edge_weight(node) + node.edge_weight(m))
            del n.adjacent_dict[node]
        del self.graph[node.index]


    def vertex_coord(self, nodes_number):
        return [(nodes_number * math.cos(2 * math.pi * i / nodes_number),
                     nodes_number * math.sin(2 * math.pi * i / nodes_number)) for i in range(nodes_number)]

    def plotter(self, mode = "standard", name = "graph"):
        nodes_list = list(self.graph.keys())
        nodes_number = len(nodes_list)
        vertexes = self.vertex_coord(nodes_number)
        preamble = "\\RequirePackage{luatex85}\n" \
                   "\\documentclass{article} \n" \
                   "\\usepackage[paperwidth=5700mm, paperheight=5700mm]{geometry} \n" \
                   "\\usepackage{tkz-graph}\n" \
                   "\\begin{document}\n" \
                   "\\thispagestyle{empty}"
        starting = "\\begin{figure}\n " \
                   "\\centering \n" \
                   "\\resizebox{\\columnwidth}{!}{\n" \
                   "\\begin{tikzpicture} \n " \
                   "\\tikzstyle{EdgeStyle}=[pre] \n"

        if mode == "standard":
            nodes, edges = self.show_graph(nodes_list, vertexes)
        if mode == "dijkstra":
            nodes, edges = self.show_dijkstra(nodes_list, vertexes)
        if mode == "path":
            end = input("Enter node index you want to reach: ")
            nodes, edges = self.show_path(nodes_list, vertexes, int(end))


        ending ="\\end{tikzpicture}} \n" \
                "\\end{figure}"
        formula = starting + nodes + edges + ending
        preview(formula, output='pdf', viewer='file', filename=f'{name}.pdf', euler=False, preamble=preamble)

    def show_graph(self, nodes_list, vertexes):
        """
        Renders graph into LaTeX image.
        Parameters

        """
        nodes = str()
        edges = str()
        for i in range(len(nodes_list)):
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]}] { {nodes_list[i]} } \n"
            connections = self.graph[nodes_list[i]].get_connections_indexes()
            for j in connections:
                if j == nodes_list[i]:
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({nodes_list[i]}) \n"
                else:
                    edges = edges + f"\\Edge[label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({j})({nodes_list[i]}) \n"
        return nodes, edges



    def show_dijkstra(self, nodes_list, vertexes):
        """
        Renders graph into LaTeX image.
        Parameters

        """
        nodes = str()
        edges = str()
        for i in range(len(nodes_list)):
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]},L=${self.graph[nodes_list[i]].dijkstra_distance}$] { {nodes_list[i]} } \n"
            connections = self.graph[nodes_list[i]].get_connections_indexes()
            for j in connections:
                if j == nodes_list[i]:
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({nodes_list[i]}) \n"
                else:
                    edges = edges + f"\\Edge[label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({j})({nodes_list[i]}) \n"
        return nodes, edges

    def show_path(self, nodes_list, vertexes, end):
        """
        Renders in red in the graph the path to a node.
        Parameters
        ----------
        end Aimed node
        -------

        """
        nodes = str()
        edges = str()
        path = self._get_path(self.get_node(end))  # Collect the path to the node
        path.reverse()
        for i in range(len(nodes_list)):  # For all the node in the graph
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]}] { {nodes_list[i]} } \n"  # Add the nodes
            connections = self.graph[nodes_list[i]].get_connections_indexes()  # For all nodes, make a list of the edges
            for j in connections:  # For all the ending node of the edges of th node studied at the moment
                if j == nodes_list[i]:  # If the node end where it starts, make a loop
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({nodes_list[i]}) \n"
                else:
                    if self.get_node(nodes_list[i]) in path and self.get_node(j) in path:  # If the starting and ending node are both in path (they are surely subsiquent)
                        edges = edges + f"\\Edge[label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$, color=red]({j})({nodes_list[i]}) \n"
                        path.remove(self.get_node(nodes_list[i]))
                    else:
                        edges = edges + f"\\Edge[label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({j})({nodes_list[i]}) \n"
        return nodes, edges




