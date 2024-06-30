
import sys
import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

# Lista de aeropuertos para referencia
airports = ["CCS", "AUA", "CUR", "BON", "SXM", "SDQ", "POS", "BGI", "PTP", "FDF", "SBH"]

# Requisitos de visa
visa_required = {"AUA", "BON", "CUR", "SXM", "SDQ"}

# Nombre del archivo
filename = "matriz.txt"

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

def has_visa(airport, tiene_visa):
    return not (airport in visa_required and not tiene_visa)

def dijkstra(graph, start, end, tiene_visa):
    if not has_visa(start, tiene_visa) or not has_visa(end, tiene_visa):
        return None
    
    # Inicializar las distancias a todos los nodos como infinitas y la distancia al inicio como 0
    distances = {node: sys.maxsize for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    nodes = list(graph.keys())
    
    while nodes:
        # Encontrar el nodo con la menor distancia conocida
        current_node = min(nodes, key=lambda node: distances[node])
        nodes.remove(current_node)
        
        if distances[current_node] == sys.maxsize:
            break
        
        for neighbor, cost in graph[current_node].items():
            if not has_visa(neighbor, tiene_visa):
                continue
            alternative_route = distances[current_node] + cost
            if alternative_route < distances[neighbor]:
                distances[neighbor] = alternative_route
                previous_nodes[neighbor] = current_node

    # Reconstruir el camino desde el nodo final al nodo de inicio
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path = path[::-1]  # Invertir el camino

    return distances[end], path

def count_stops(path):
    return len(path) - 2  # El número de escalas es el número de nodos en el camino menos 2 (inicio y fin)

def mostrar_grafo(graph):
    G = nx.DiGraph()
    for node in graph:
        for neighbor, cost in graph[node].items():
            G.add_edge(node, neighbor, weight=cost)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

def buscar_ruta():
    start = entry_start.get()
    end = entry_end.get()
    tiene_visa = bool_var.get()
    
    if start not in graph or end not in graph:
        messagebox.showerror("Error", "Aeropuertos inválidos. Por favor ingrese aeropuertos válidos.")
        return
    
    ruta_mas_barata = dijkstra(graph, start, end, tiene_visa)
    
    if ruta_mas_barata:
        cost, path = ruta_mas_barata
        stops = count_stops(path)
        result_text.set(f"Ruta más barata: {path} con costo de {cost}\nNúmero de escalas: {stops}")
    else:
        result_text.set("No se puede encontrar una ruta debido a restricciones de visa o datos inválidos.")
