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

    def edge_weight(self, connected_node: Generic) -> bool:
        """
        Function which returns the weight of the edge to a specific node.
        Parameters
        ----------
        connected_node: the connected node whose edge we are interested in

        Returns: the weight of the edge
        -------

        """
        return self.adjacent_dict[connected_node]

    def edge_weight_number(self, connected_node: Generic) -> bool:
        """
        Function which returns the weight of the edge to a specific node.
        Parameters
        ----------
        connected_node: the connected node whose edge we are interested in

        Returns: the weight of the edge
        -------

        """
        return self.adjacent_dict[connected_node]

    def set_distance(self, d: bool) -> None:
        self.dijkstra_distance = d


    def set_pred(self, pred: Generic) -> None:
        self.dijkstra_pred = pred



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
        Function which returns a node in the graph
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
        Function which create an edge between two nodes
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
        Returns: list of all the nodes in the graph
        -------

        """
        return self.graph.keys()

    def get_nodes_list(self) -> list:
        """
        Function which return a list of the index of all the nodes in the graph
        Returns: list of all the nodes in the graph
        -------

        """
        return list(self.graph.keys())

    def get_distance_node(self, index: int):
        return self.get_node(index).dijkstra_distance

    def get_distances(self):
        distances = [self.get_node(v).dijkstra_distance for v in self.graph]
        return distances

    def get_pred(self):
        pred = [self.get_node(v).dijkstra_pred for v in self.graph]
        return pred

    def _get_path(self, end):
        path = [end]
        while end.dijkstra_pred != None:
            path.append(end.dijkstra_pred)
            end = end.dijkstra_pred
        return path




    def show_graph(self):
        """
        Renders graph into LaTeX image.
        Parameters

        """
        nodes_list = list(self.graph.keys())
        nodes_number = len(nodes_list)
        vertexes = [(nodes_number * math.cos(2 * math.pi * i / nodes_number),
                     nodes_number * math.sin(2 * math.pi * i / nodes_number)) for i in range(nodes_number)]
        preamble =  "\\RequirePackage{luatex85}\n" \
                    "\\documentclass{article} \n" \
                    "\\usepackage[paperwidth=5700mm, paperheight=5700mm]{geometry} \n" \
                    "\\usepackage{tkz-graph}\n" \
                    "\\begin{document}\n" \
                    "\\thispagestyle{empty}"
        starting =  "\\begin{figure}\n " \
                    "\\centering \n" \
                    "\\resizebox{\\columnwidth}{!}{\n" \
                    "\\begin{tikzpicture} \n " \
                    "\\tikzstyle{EdgeStyle}=[pre] \n"
        nodes = str()
        for i in nodes_list:
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]}] { {i} } \n"
        edges = str()
        for i in nodes_list:
            connections = self.graph[i].get_connections_indexes()
            for j in connections:
                if j == i:
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=${self.graph[i].edge_weight(self.graph[connections[j]])}$]({i}) \n"
                else:
                    edges = edges + f"\\Edge[label=${self.graph[i].edge_weight(self.graph[j])}$]({j})({i}) \n"
        ending ="\\end{tikzpicture}} \n" \
                "\\end{figure}"
        formula = starting + nodes + edges + ending
        preview(formula, output='pdf', viewer='file', filename='graph.pdf', euler=False, preamble=preamble)


    def show_dijkstra(self):
        """
        Renders graph into LaTeX image.
        Parameters

        """
        nodes_list = list(self.graph.keys())
        nodes_number = len(nodes_list)
        vertexes = [(nodes_number * math.cos(2 * math.pi * i / nodes_number),
                     nodes_number * math.sin(2 * math.pi * i / nodes_number)) for i in range(nodes_number)]
        preamble =  "\\RequirePackage{luatex85}\n" \
                    "\\documentclass{article} \n" \
                    "\\usepackage[paperwidth=5700mm, paperheight=5700mm]{geometry} \n" \
                    "\\usepackage{tkz-graph}\n" \
                    "\\begin{document}\n" \
                    "\\thispagestyle{empty}"
        starting =  "\\begin{figure}\n " \
                    "\\centering \n" \
                    "\\resizebox{\\columnwidth}{!}{\n" \
                    "\\begin{tikzpicture} \n " \
                    "\\tikzstyle{EdgeStyle}=[pre] \n"
        nodes = str()
        for i in nodes_list:
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]},L=${self.graph[i].dijkstra_distance}$] { {i} } \n"
        edges = str()
        for i in nodes_list:
            connections = self.graph[i].get_connections_indexes()
            for j in connections:
                if j == i:
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=${self.graph[i].edge_weight(self.graph[connections[j]])}$]({i}) \n"
                else:
                    edges = edges + f"\\Edge[label=${self.graph[i].edge_weight(self.graph[j])}$]({j})({i}) \n"
        ending ="\\end{tikzpicture}} \n" \
                "\\end{figure}"
        formula = starting + nodes + edges + ending
        preview(formula, output='pdf', viewer='file', filename='graph_distances.pdf', euler=False, preamble=preamble)

    def show_path(self, start, end):
        """
        Renders graph into LaTeX image.
        Parameters

        """
        nodes_list = list(self.graph.keys())
        nodes_number = len(nodes_list)
        vertexes = [(nodes_number * math.cos(2 * math.pi * i / nodes_number),
                     nodes_number * math.sin(2 * math.pi * i / nodes_number)) for i in range(nodes_number)]
        preamble =  "\\RequirePackage{luatex85}\n" \
                    "\\documentclass{article} \n" \
                    "\\usepackage[paperwidth=5700mm, paperheight=5700mm]{geometry} \n" \
                    "\\usepackage{tkz-graph}\n" \
                    "\\begin{document}\n" \
                    "\\thispagestyle{empty}"
        starting =  "\\begin{figure}\n " \
                    "\\centering \n" \
                    "\\resizebox{\\columnwidth}{!}{\n" \
                    "\\begin{tikzpicture} \n " \
                    "\\tikzstyle{EdgeStyle}=[pre] \n"
        nodes = str()
        for i in nodes_list:
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]},L=${self.graph[i].dijkstra_distance}$] { {i} } \n"
        path = self._get_path(self.get_node(start), self.get_node(end))
        for i in path:
            print(i.index)
        print(path)
        edges = str()
        for i in nodes_list:
            connections = self.graph[i].get_connections_indexes()
            for j in connections:
                if j == i:
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=${self.graph[i].edge_weight(self.graph[connections[j]])}$]({i}) \n"
                else:
                    if (self.get_node(i) and self.get_node(j)) in path:
                        edges = edges + f"\\Edge[label=${self.graph[i].edge_weight(self.graph[j])}$, color=red]({j})({i}) \n"
                        path.remove(self.get_node(j))
                    else:
                        edges = edges + f"\\Edge[label=${self.graph[i].edge_weight(self.graph[j])}$]({j})({i}) \n"
        ending ="\\end{tikzpicture}} \n" \
                "\\end{figure}"
        formula = starting + nodes + edges + ending
        preview(formula, output='pdf', viewer='file', filename='graph_path.pdf', euler=False, preamble=preamble)




