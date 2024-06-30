# graph_utils.py

import networkx as nx
import matplotlib.pyplot as plt

airports = ["CCS", "AUA", "CUR", "BON", "SXM", "SDQ", "POS", "BGI", "PTP", "FDF", "SBH"]

visa_required = {"AUA", "BON", "CUR", "SXM", "SDQ"}

def read_adjacency_matrix(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        matrix = []
        for line in lines:
            matrix.append(list(map(int, line.strip().split())))
        return matrix

def create_graph(matrix):
    graph = {}
    for i in range(len(matrix)):
        graph[airports[i]] = {}
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                graph[airports[i]][airports[j]] = matrix[i][j]
    return graph

def mostrar_grafo(graph, path=None):
    G = nx.DiGraph()
    for node in graph:
        for neighbor, cost in graph[node].items():
            G.add_edge(node, neighbor, weight=cost)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

    plt.show()
