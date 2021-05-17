from typing import TypeVar, KeysView, Optional, List, Generic
import copy
from sympy import *
import math

K = TypeVar('K')


class Node(Generic[K]):
    """
    Adjacency list representation of a weighted graph node, implemented using a python dictionary
    """

    def __init__(self, vertex: int):
        self.index = vertex
        self.adjacent_dict = {}
        self.dijkstra_distance = None
        self.dijkstra_pred = None
        self.importance = None
        self.hierarchy = None
        self.binheap_index = None

    def __str__(self) -> str:
        return str(self.index) + ' adjacent: ' + str([x.index for x in self.adjacent_dict])

    def add_connected_node(self, connected_node: Generic[K], weight: K = 1) -> None:
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

        Returns
        -------
        Keys of the adjacency list dictionary

        """
        return self.adjacent_dict.keys()

    def get_connections_indexes(self) -> List:
        """
        Function which returns the indexes of the connected nodes

        Returns:
        -------
        Keys of the adjacency list dictionary

        """
        return [x.index for x in self.adjacent_dict]

    def edge_weight(self, connected_node: Generic[K]) -> K:
        """
        Function which returns the weight of the edge to a specific node.

        Parameters
        ----------
        connected_node the connected node whose edge we are interested in

        Returns
        -------
        The weight of the edge
        """
        return self.adjacent_dict[connected_node]

    def set_distance(self, d: K) -> None:
        """
        Function which set the attribute dijkstra_distance to the distance of the node from the origin
        during an application of the dijkstra algorithm

        Parameters
        ----------
        d the distance calculated by the dijkstra algorithm
        -------

        """
        self.dijkstra_distance = d

    def set_pred(self, pred: int) -> None:
        """
        Function which set the attribute dijkstra_pred to the index of the precedent node found
        according to an application of the dijkstra algorithm

        Parameters
        ----------
        pred the index of the precedent node calculated by the dijkstra algorithm
        -------

        """
        self.dijkstra_pred = pred

    def set_importance(self, importance: K) -> None:
        """
        Function which set the attribute importance to the desired value calculated heuristically, it is used
        for the evaluation of the contraction hierarchies

        Parameters
        ----------
        importance importance of the node
        -------

        """
        self.importance = importance


class Graph(Generic[K]):
    """
    Adjacency list representation of a weighted graph,implemented using a python dictionary
    """

    def __init__(self, A: Optional[dict] = None):
        if A is None:
            self.length_graph = 0
            self.graph = {}
        elif isinstance(A, int):
            self.length_graph = 0
            self.graph = {A}
        else:
            self.length_graph = len(A)
            self.graph = A

    def __iter__(self):
        return iter(self.graph.values())

    def add_node(self, index: int) -> Generic[K]:
        """
        Function which add a new node with a given index to the graph

        Parameters
        ----------
        index index of the new node

        Returns
        -------
        The node
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
        index index of the node of interest

        Returns
        -------
        The node of interest

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

        Returns
        -------
        List of all the nodes in the graph.

        """
        return self.graph.keys()

    def get_nodes_list(self) -> List:
        """
        Function which returns a list of the index of all the nodes in the graph

        Returns
        -------
        List of all the nodes in the graph.
        """
        return list(self.graph.keys())

    def get_distances(self) -> List:
        """
        After an application of the Dijkstra algorithm, the function which returns a list of the distances
        of all nodes from the origin.
        """
        distances = [self.get_node(v).dijkstra_distance for v in self.graph]
        return distances

    def get_pred(self) -> List:
        """
        Function which return the list of the precedent node for all the nodes in the graph.
        """
        pred = [self.get_node(v).dijkstra_pred for v in self.graph]
        return pred

    @staticmethod
    def _get_path(end) -> List:
        """
        After an application of the Dijkstra algorithm, the function return the node path from the origin
        to the node given in input.

        Parameters
        ----------
        end Aimed node
        -------

        """
        path = [end]
        while end.dijkstra_pred is not None:
            path.append(end.dijkstra_pred)
            end = end.dijkstra_pred
        return path

    def copy(self):
        """
        Performs a deep copy of the graph

        Returns
        -------
        Deep copy of the graph

        """
        return copy.deepcopy(self)

    def remove_node(self, node: Generic[K]) -> None:
        """
        Function which removes a node creating shortcuts between the remaining ones.

        Parameters
        ----------
        node The node to remove
        -------

        """
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
            # Delete the node, and all its references in the adjacent_dict of all the others nodes
            del n.adjacent_dict[node]
        del self.graph[node.index]

    def just_node(self, index: int) -> None:
        """
        Function which removes from the graph all the nodes except the ones which shares an edge with the node given
        in input

        Parameters
        ----------
        index index of the input node
        -------

        """
        node = self.get_node(index)
        to_erase = []
        # Get all the node to pop
        for i in self.graph:
            if (self.get_node(i) != node) and (self.get_node(i) not in node.adjacent_dict) and (
                    node not in self.get_node(i).adjacent_dict):
                to_erase.append(i)
        # Pop all the useless edges
        for i in self.graph:
            edge_to_erase = []
            for j in self.get_node(i).adjacent_dict:
                if j.index in to_erase:
                    edge_to_erase.append(j.index)
            for j in edge_to_erase:
                self.get_node(i).adjacent_dict.pop(self.get_node(j), None)
        # Pop all the nodes
        for i in to_erase:
            self.graph.pop(i, None)

    @staticmethod
    def vertex_coord(nodes_number: int) -> List:
        """
        Function which, given a number of nodes as input, returns a list of pairs of coordinates to place them
        on the edge of a regular shape

        Parameters
        ----------
        nodes_number number of required nodes

        Returns
        -------
        List of coordinates pairs

        """
        return [(nodes_number * math.cos(2 * math.pi * i / nodes_number),
                 nodes_number * math.sin(2 * math.pi * i / nodes_number)) for i in range(nodes_number)]

    def plotter(self, mode: str = "standard", name: str = "graph", display: str = 'file') -> None:
        """
        Function which plot the graph as Latex image. It accept different kinds of input depending on the required plot.
        Because of the Latex compiling time limitation, the function might find some difficulties in rendering very
        large graphs, or very connected graph
        Parameters
        ----------
        mode Kind of plot required
        name Name to give to the output file
        display How the image is displayed. Choose None to automatically open the image at the end of the computation.
        -------

        """
        nodes_list = list(self.graph.keys())
        vertexes = self.vertex_coord(len(nodes_list))
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

        if mode == "standard":
            text = self.show_graph(nodes_list, vertexes)
        elif mode == "dijkstra":
            text = self.show_dijkstra(nodes_list, vertexes)
        elif mode == "importance":
            text = self.show_importance(nodes_list, vertexes)
        elif mode == "path":
            end = input("Enter node index you want to reach: ")
            text = self.show_path(nodes_list, vertexes, int(end))
        else:
            raise RuntimeError(f'{mode} is not an available plot')

        ending = "\\end{tikzpicture}} \n" \
                 "\\end{figure}"
        formula = starting + text + ending
        preview(formula, output='pdf', viewer=display, filename=f'{name}.pdf', euler=False, preamble=preamble)

    def show_graph(self, nodes_list: List, vertexes: List) -> str:
        """
        Utility function to get the latex text to renders the graph into LaTeX image.

        Parameters
        ----------
        nodes_list List of nodes in the graph
        vertexes List of the coordinates of each node

        Returns
        -------
        Latex string

        """
        nodes = str()
        edges = str()
        for i in range(len(nodes_list)):
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]}] { {nodes_list[i]} } \n"
            connections = self.graph[nodes_list[i]].get_connections_indexes()
            for j in connections:
                if j == nodes_list[i]:
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=$" \
                                    f"{self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({nodes_list[i]}) \n"
                else:
                    edges = edges + f"\\Edge[label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$](" \
                                    f"{j})({nodes_list[i]}) \n"
        return nodes + edges

    def show_dijkstra(self, nodes_list: List, vertexes: List) -> str:
        """
        Utility function to get the latex text to renders the graph into LaTeX image,
        indicating for each node its dijkstra distance.

        Parameters
        ----------
        nodes_list List of nodes in the graph
        vertexes List of the coordinates of each node

        Returns
        -------
        Latex string

        """
        nodes = str()
        edges = str()
        for i in range(len(nodes_list)):
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]}," \
                            f"L=${self.graph[nodes_list[i]].dijkstra_distance}$] { {nodes_list[i]} } \n"
            connections = self.graph[nodes_list[i]].get_connections_indexes()
            for j in connections:
                if j == nodes_list[i]:
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=$" \
                                    f"{self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({nodes_list[i]}) \n"
                else:
                    edges = edges + f"\\Edge[label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({j})" \
                                    f"({nodes_list[i]}) \n"
        return nodes + edges

    def show_path(self, nodes_list: List, vertexes: List, end: int) -> str:
        """
        Utility function to get the latex text to renders the graph into LaTeX image, showing in red in the graph
        the path to a node given in input (after an the dijkstra algorithm was applied). Requires an user input
        for the aimed node.

        Parameters
        ----------
        nodes_list List of nodes in the graph
        vertexes List of the coordinates of each node
        end index of the end-node of interest

        Returns
        -------
        Latex string
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
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=$" \
                                    f"{self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({nodes_list[i]}) \n"
                else:
                    if self.get_node(nodes_list[i]) in path and self.get_node(
                            j) in path:  # If the starting and ending node are both in path (they are surely subsiquent)
                        edges = edges + f"\\Edge[label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$," \
                                        f" color=red]({j})({nodes_list[i]}) \n"
                        path.remove(self.get_node(nodes_list[i]))
                    else:
                        edges = edges + f"\\Edge[label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]" \
                                        f"({j})({nodes_list[i]}) \n"
        return nodes + edges

    def show_importance(self, nodes_list: List, vertexes: List) -> str:
        """
        Utility function to get the latex text to renders the graph into LaTeX image,
        indicating for each node its importance.

        Parameters
        ----------
        nodes_list List of nodes in the graph
        vertexes List of the coordinates of each node

        Returns
        -------
        Latex string
        """
        nodes = str()
        edges = str()
        for i in range(len(nodes_list)):
            nodes = nodes + f"\\Vertex[x={vertexes[i][0]},y={vertexes[i][1]}," \
                            f"L=${self.graph[nodes_list[i]].importance}$] { {nodes_list[i]} } \n"
            connections = self.graph[nodes_list[i]].get_connections_indexes()
            for j in connections:
                if j == nodes_list[i]:
                    edges = edges + f"\\Loop[dir=NO,dist=2cm,label=$" \
                                    f"{self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]({nodes_list[i]}) \n"
                else:
                    edges = edges + f"\\Edge[label=${self.graph[nodes_list[i]].edge_weight(self.graph[j])}$]" \
                                    f"({j})({nodes_list[i]}) \n"
        return nodes + edges
