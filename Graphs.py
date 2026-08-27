# Graphs
# DQ

from random import randint
from Data_Structures import Circular_Queue, Stack

##############################################################################################
# all values which come from outside the classes below have been validated within the classes
##############################################################################################

class Node:
    __MAX_NO_CONNECTIONS = 4
    
    def __init__(self, name):
        self.__name = name
        self.__connections = []

    def __len__(self):
        return len(self.__connections)

    ######################################
    # decorator
    # validates input for 'connect' method
    ######################################
    def __check_node(func):
        def inner(*args):
            match args[1]:
                case Node():
                    return func(*args)
        return inner

    @classmethod
    @property
    def MAX_NO_CONNECTIONS(cls):
        return cls.__MAX_NO_CONNECTIONS

    @property
    def name(self):
        return self.__name

    @property
    def connections(self):
        return self.__connections
    
    ######################################################
    # return True if Node can be connected to another Node
    # otherwise return False
    ######################################################
    @property 
    def is_available(self):
        return len(self) < Node.__MAX_NO_CONNECTIONS

    @__check_node
    def connect(self, node):
        if node not in self.__connections:
            self.__connections.append(node)

class Tree:

    def __init__(self):
        self.__nodes = []
        self.__connections = []

    # decorator
    def __check_node(func):
        def inner(*args):
            match args[1]:
                case [item_1, item_2]:
                    if isinstance(item_1, Node) and isinstance(item_2, Node):
                        return func(*args)
        return inner

    @__check_node
    def connect_nodes(self, nodes):
        if nodes[0] in self.__nodes and nodes[1] in self.__nodes:
            if not self.__depth_first_search(nodes[0], nodes[1]):
                self.__connections.append(nodes)
                return True
            return False
        if nodes[0] not in self.__nodes:
            self.__nodes.append(nodes[0])
        if nodes[1] not in self.__nodes:
            self.__nodes.append(nodes[1])
        self.__connections.append(nodes)
        return True

    def __depth_first_search(self, start_node, target_node):
        fully_explored = []
        visited = Stack()
        visited.push(start_node)
        while not visited.is_empty:
            node = visited.peek()
            connection_found = False
            i = 0
            while not connection_found and i < len(self.__connections):
                if node in self.__connections[i]:
                    connection_found = True
                    if target_node in self.__connections[i]:
                        return True
                    if not self.__check_repeating_arc(visited.peek_2(), self.__connections[i]):
                        if self.__connections[i][0] == node and self.__connections[i][1] not in fully_explored:
                                visited.push(self.__connections[i][1])
                        elif self.__connections[i][1] == node and self.__connections[i][0] not in fully_explored:
                            visited.push(self.__connections[i][0])
                        else:
                            connection_found = False
                    else:
                        connection_found = False
                i += 1
            if not connection_found:
                fully_explored.append(visited.pop())
        return False
    
    def __check_repeating_arc(self, items_1, items_2):
        if items_1 and items_2:
            if len(items_1) == 2:
                return items_1[0] in items_2 and items_1[1] in items_2

class Graph:
    __LACK_CONNECTION = 999
    __UNCONNECTABLE = 1000
    __MIN_WEIGHT = 10
    __MAX_WEIGHT = 100
    __MIN_NO_NODES = 4
    __MAX_NO_NODES = 8

    def __init__(self, no_nodes):
        no_nodes = self._set_no_nodes(no_nodes)
        self.__adjacency_matrix = [[Graph.__LACK_CONNECTION if i != j else Graph.__UNCONNECTABLE for i in range(no_nodes)] for j in range(no_nodes)]
        self.__nodes = tuple((Node(chr(65+i)) for i in range(no_nodes)))
        self.__make_graph()

    def __len__(self):
        return len(self.__nodes)

    @classmethod
    @property
    def LACK_CONNECTION(cls):
        return cls.__LACK_CONNECTION

    @classmethod
    @property
    def _UNCONNECTABLE(cls):
        return cls.__UNCONNECTABLE

    @classmethod
    @property
    def MIN_NO_NODES(cls):
        return cls.__MIN_NO_NODES

    @classmethod
    @property
    def MAX_NO_NODES(cls):
        return cls.__MAX_NO_NODES

    @property
    def adjacency_matrix(self):
        return self.__adjacency_matrix

    @property
    def nodes(self):
        return self.__nodes

    def weight(self, i, j):
        return self.__adjacency_matrix[i][j]
    
    def _set_no_nodes(self, no_nodes):
        match no_nodes:
            case int() if Graph.__MIN_NO_NODES <= no_nodes <= Graph.__MAX_NO_NODES:
                return no_nodes
            case str():
                try:
                    return self._set_no_nodes(int(no_nodes))
                except:
                    return randint(Graph.__MIN_NO_NODES, Graph.__MAX_NO_NODES)
        return randint(Graph.__MIN_NO_NODES, Graph.__MAX_NO_NODES)
    
    def __make_graph(self):
        self._populate()
        connected_nodes = self.__breadth_first_traverse() 
        available_nodes = []
        unconnected_nodes = []
        for i in range(len(self)):
            if self.__nodes[i] in connected_nodes:
                if self.__nodes[i].is_available:
                    available_nodes.append(self.__nodes[i])
            else:
                unconnected_nodes.append(self.__nodes[i])
        if unconnected_nodes:
            self.__make_connected(connected_nodes, unconnected_nodes)

    
    def _populate(self):
        for i in range(len(self)):
            for j in range(i+1, len(self)):
                if (
                    self.__nodes[i].is_available and self.__nodes[j].is_available and 
                    randint(1, len(self)) <= Node.MAX_NO_CONNECTIONS - len(self.__nodes[i])
                    ): 
                    self.__fill(i, j)

    def __fill(self, i, j):
        self.__adjacency_matrix[i][j] = randint(Graph.__MIN_WEIGHT, Graph.__MAX_WEIGHT)
        self.__adjacency_matrix[j][i] = self.__adjacency_matrix[i][j]
        self.__nodes[i].connect(self.__nodes[j])
        self.__nodes[j].connect(self.__nodes[i])

    def __breadth_first_traverse(self):
        fully_explored = []
        start_node = self.__nodes[0]
        visited = Circular_Queue()
        visited.enqueue([new_node for new_node in start_node.connections if new_node not in visited.items and new_node not in fully_explored], True)
        fully_explored.append(start_node)
        while not visited.is_empty:
            node = visited.dequeue()
            visited.enqueue([new_node for new_node in node.connections if new_node not in visited.items and new_node not in fully_explored], True)
            fully_explored.append(node)
        return fully_explored
    
    def __make_connected(self, connected_nodes, unconnected_nodes):
        available_nodes = Circular_Queue()
        available_nodes.enqueue(connected_nodes, True)
        for i in range(len(unconnected_nodes)):
            available_node = available_nodes.dequeue()
            self.__fill(self.__nodes.index(unconnected_nodes[i]), self.__nodes.index(available_node))
            if available_node.is_available:
                available_nodes.enqueue(available_node)
            if unconnected_nodes[i].is_available:
                available_nodes.enqueue(unconnected_nodes[i])

class Floyds_Graph(Graph):

    def __init__(self, no_nodes):
        super().__init__(no_nodes)
        self.__route_matrices = [[[self.nodes[i].name for i in range(len(self))] for j in range(len(self))]]

        self.__distance_matrices = [[[self.adjacency_matrix[j][i] for i in range(len(self))] for j in range(len(self))]]
        self.__changes = [[[False for _ in range(len(self))] for _ in range(len(self))]]
        self.__perform_floyds(0, 0, 1)

    @property
    def changes(self):
        return self.__changes

    def weights(self, i):
        return self.__distance_matrices[i]

    def get_change(self, i, j, k):
        return self.__changes[i][j][k]

    def get_path_weight(self, i, j, k):
        return self.__distance_matrices[i][j][k]

    def get_path(self, i, j, k):
        return self.__route_matrices[i][j][k]

    def __perform_floyds(self, i, j, k):
        if k != len(self):
            if i != j != k != i:
                row_column = self.__distance_matrices[i][j][k]
                column = self.__distance_matrices[i][i][k]
                row = self.__distance_matrices[i][j][i]
                if (
                    column + row < row_column
                    ):
                    self.__distance_matrices[i][j][k] = row + column
                    self.__route_matrices[i][j][k] = self.__route_matrices[i][j][i]
                    self.__changes[i][j][k] = True
                    self.__distance_matrices[i][k][j] = row + column
                    self.__route_matrices[i][k][j] = self.__route_matrices[i][k][i]
                    self.__changes[i][k][j] = True
            self.__perform_floyds(i, j, k+1)
        elif j != len(self) - 1:
            self.__perform_floyds(i, j+1, j+1)
        elif i != len(self) -1:
            self.__distance_matrices.append([[self.__distance_matrices[i][k][j] for j in range(len(self))] for k in range(len(self))])
            self.__changes.append([[False for _ in range(len(self))] for _ in range(len(self))])
            self.__route_matrices.append([[self.__route_matrices[i][k][j] for j in range(len(self))] for k in range(len(self))])
            self.__perform_floyds(i+1, 0, 1)
        
class Kruskals_Graph(Graph):

    def __init__(self, no_nodes):
        super().__init__(no_nodes)
        while len(self.__get_arcs()) == len(self) -1:
            self._populate() 

        self.__arcs = self.__get_arcs()
        self.__no_arcs = len(self.__arcs)
        self.__sorted_arcs = {}
        self.__selected_arcs = {}
        self.__connected_nodes = []
        self.__perform_kruskal()

    @property
    def selected_arcs(self):
        return self.__selected_arcs
    
    @property
    def arcs(self):
        return self.__sorted_arcs

    @property
    def no_arcs(self):
        return self.__no_arcs
    
    def __get_arcs(self):
        arcs = {}
        keys = {}
        nodes = self.nodes
        for i in range(len(self)):
            for j in range(i+1, len(self)):
                weight = self.weight(i, j)
                if weight < Kruskals_Graph.LACK_CONNECTION:
                    value = keys.get(weight)
                    if not value:
                        value = 0
                    arcs[(weight, value)] = (nodes[i], nodes[j])
                    keys[weight] = value + 1
        return arcs
    
    def __perform_kruskal(self):
        self.__mergesort()
        self.__select_arcs()

    # mergesort part 1
    def __mergesort(self):
        arcs = list(self.__arcs.keys())
        step = 2
        for _ in range(len(arcs)//2 + 1):
            j = 0
            new_arcs = []
            while len(new_arcs) != len(arcs) and j < len(arcs) * 2:
                if j + step <= len(arcs):
                    new_arcs += self.__merge(arcs[j:j+step//2], arcs[j+step//2:j+step])
                elif j <= len(arcs):
                    if len(new_arcs) == len(arcs) -1 and step < len(arcs):
                        new_arcs.append(arcs[len(arcs)-1])
                    else:
                        new_arcs += self.__merge(arcs[j:j+step//2], arcs[j+step//2:])
                j += step
            arcs = new_arcs
            step *= 2
        self.__sorted_arcs = {new_arcs[i]:self.__arcs[new_arcs[i]] for i in range(len(new_arcs))}

    # mergesort part 2
    def __merge(self, list_1, list_2):
        merged_list = []
        while list_1 and list_2:
            if list_1[0][0] <= list_2[0][0]:
                merged_list.append(list_1[0])
                del list_1[0]
            else:
                merged_list.append(list_2[0])
                del list_2[0]
        if list_1:
            merged_list += list_1
        elif list_2:
            merged_list += list_2
        return merged_list
    
    ######################################################
    # form tree from list of arcs in asc order
    # uses programmer-defined tree object and tree methods
    ######################################################
    def __select_arcs(self):
        items = list(self.__sorted_arcs.items())
        tree = Tree()
        i = 0
        j = 0
        while len(self) -1 != i and self.__no_arcs != j:
            if tree.connect_nodes(items[j][1]):
                self.__selected_arcs[items[j][0]] = self.__sorted_arcs[items[j][0]]
                self.__connected_nodes += self.__selected_arcs[items[j][0]]
                i += 1
            else:
                self.__selected_arcs[items[j][0]] = False
            j += 1
        for i in range(j, self.__no_arcs):
            self.__selected_arcs[items[i][0]] = False
