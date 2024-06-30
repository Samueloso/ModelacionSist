import tkinter as tk
from graph_utils import read_adjacency_matrix, create_graph
from ui import RouteFinderApp

# Nombre del archivo
filename = "matriz.txt"

# Leer y crear el grafo
matrix = read_adjacency_matrix(filename)
graph = create_graph(matrix)

# Crear la interfaz gráfica
root = tk.Tk()
app = RouteFinderApp(root, graph)
root.mainloop()