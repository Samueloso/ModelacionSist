import sys
from graph_utils import visa_required

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