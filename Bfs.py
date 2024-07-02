from graph_utils import visa_required
from collections import deque

def has_visa(airport, tiene_visa):
    return not (airport in visa_required and not tiene_visa)

def busqueda_en_anchura(graph, start, end, tiene_visa):
    if not has_visa(start, tiene_visa) or not has_visa(end, tiene_visa):
        return None

    # Crear una cola auxiliar
    queue = deque([[start]])

    # Un set para los nodos visitados
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        # Si este nodo no ha sido visitado
        if node not in visited:            
            vecinos = graph[node].keys()

            # Recorrer todos los vecinos
            for veci in vecinos:
                new_path = list(path)
                new_path.append(veci)
                queue.append(new_path)

                # Retornar la ruta si el vecino es el destino buscado
                if veci == end:
                    return calculate_cost(graph, new_path), new_path

            # Marcar el nodo como visitado
            visited.add(node)

    return None  

def calculate_cost(graph, path):
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]][path[i + 1]]
    return cost