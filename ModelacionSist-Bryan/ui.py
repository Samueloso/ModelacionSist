# ui.py
import tkinter as tk
from tkinter import messagebox
from graph_utils import mostrar_grafo, airports
from dijkstra import dijkstra, count_stops
import matplotlib.pyplot as plt
from Bfs import busqueda_en_anchura

class RouteFinderApp:
    def __init__(self, root, graph, graph_aux):
        self.root = root
        self.graph = graph
        self.graph_aux = graph_aux
        self.root.title("Buscador de Rutas de Vuelos")

        # Ajustar el tamaño de la ventana
        self.root.geometry("600x400")
        self.centrar_ventana(600, 400)

        # Configurar el grid para centrar los elementos
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_rowconfigure(6, weight=1)

        tk.Label(root, text="Aeropuerto de origen:").grid(row=0, column=0, sticky="e")
        self.start_var = tk.StringVar(root)
        self.start_var.set(airports[0])  # Valor por defecto
        self.start_menu = tk.OptionMenu(root, self.start_var, *airports)
        self.start_menu.grid(row=0, column=1, sticky="w")

        tk.Label(root, text="Aeropuerto de destino:").grid(row=1, column=0, sticky="e")
        self.end_var = tk.StringVar(root)
        self.end_var.set(airports[0])  # Valor por defecto
        self.end_menu = tk.OptionMenu(root, self.end_var, *airports)
        self.end_menu.grid(row=1, column=1, sticky="w")

        self.bool_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Tiene visa", variable=self.bool_var).grid(row=2, column=0, columnspan=2)

        tk.Button(root, text="Buscar Ruta más barata", command=self.buscar_ruta_barata).grid(row=3, column=0, columnspan=2)

        tk.Button(root, text="Buscar Ruta con menos escalas", command=self.buscar_ruta_corta).grid(row=4, column=0, columnspan=2)

        self.result_text = tk.StringVar()
        tk.Label(root, textvariable=self.result_text, wraplength=400).grid(row=5, column=0, columnspan=2)

        tk.Button(root, text="Mostrar Grafo", command=lambda: self.mostrar_grafo()).grid(row=6, column=0, columnspan=2)

    def buscar_ruta_barata(self):
        start = self.start_var.get()
        end = self.end_var.get()
        tiene_visa = self.bool_var.get()
        
        if start not in self.graph or end not in self.graph or start == end:
            messagebox.showerror("Error", "Aeropuertos inválidos. Por favor ingrese aeropuertos válidos.")
            return
        if tiene_visa == True:
            ruta_mas_barata = dijkstra(self.graph, start, end, tiene_visa)
        else:
            ruta_mas_barata = dijkstra(self.graph_aux, start, end, tiene_visa)

        if ruta_mas_barata:
            cost, path = ruta_mas_barata
            stops = count_stops(path)
            self.result_text.set(f"Ruta más barata: {path} con costo de {cost}\nNúmero de escalas: {stops}")
            self.mostrar_grafo(path)  # Mostrar el grafo con la ruta resaltada
        else:
            self.result_text.set("No se puede encontrar una ruta debido a restricciones de visa")

    def buscar_ruta_corta(self):
        start = self.start_var.get()
        end = self.end_var.get()
        tiene_visa = self.bool_var.get()

        if start not in self.graph or end not in self.graph or start == end:
            messagebox.showerror("Error", "Aeropuertos inválidos. Por favor ingrese aeropuertos válidos.")
            return
        
        print(tiene_visa)
        if tiene_visa == True:
            ruta_menos_escalas = busqueda_en_anchura(self.graph, start, end, tiene_visa)
        else:
            ruta_menos_escalas = busqueda_en_anchura(self.graph_aux, start, end, tiene_visa)
    
        if ruta_menos_escalas:
            cost, path = ruta_menos_escalas
            stops = count_stops(path)            
            self.result_text.set(f"Ruta con menos escalas: {path} con costo de {cost}\nNúmero de escalas: {stops}")
            self.mostrar_grafo(path)  # Mostrar el grafo con la ruta resaltada
        else:
            self.result_text.set("No se puede encontrar una ruta debido a restricciones de visa")

    def mostrar_grafo(self, path=None):
        plt.close('all')
        mostrar_grafo(self.graph, path)

    def centrar_ventana(self, width, height):
        # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calcular la posición x e y para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Establecer la geometría de la ventana
        self.root.geometry(f"{width}x{height}+{x}+{y}")
