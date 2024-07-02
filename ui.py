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

    def mostrar_info(self, titulo, mensaje):
        # Crear la ventana emergente
        ventana_emergente = tk.Toplevel(self.root)
    
        # Configurar el título de la ventana emergente
        ventana_emergente.title(titulo)
    
        # Crear un widget Label para mostrar el mensaje
        label_mensaje = tk.Label(ventana_emergente, text=mensaje)
    
        # Posicionar el widget Label en la ventana emergente
        label_mensaje.pack(padx=20, pady=20)
    
        # Botón "OK" para cerrar la ventana
        boton_ok = tk.Button(ventana_emergente, text="OK", command=lambda: ventana_emergente.destroy())
        boton_ok.pack(pady=10)
    
        # Ajustar el tamaño de la ventana emergente
        ventana_emergente.geometry('300x200')

    def buscar_ruta_barata(self):
        start = self.start_var.get()
        end = self.end_var.get()
        tiene_visa = self.bool_var.get()
        
        if start == end:
            messagebox.showwarning("Advertencia", "El inicio y el fin son el mismo aeropuerto. No hay necesidad de búsqueda.")
            return

        if tiene_visa == True:
            ruta_mas_barata = dijkstra(self.graph, start, end, tiene_visa)
        else:
            ruta_mas_barata = dijkstra(self.graph_aux, start, end, tiene_visa)

        if ruta_mas_barata:
            cost, path = ruta_mas_barata
            stops = count_stops(path)
            titulo = "Ruta más barata"
            mensaje = f"{path} con costo de ${cost}\nNúmero de escalas: {stops}"
            self.mostrar_info(titulo, mensaje)
            self.mostrar_grafo(path)  # Mostrar el grafo con la ruta resaltada

        else:
            titulo = "Visa Requerida"
            mensaje = "No se puede encontrar una ruta debido a restricciones de visa"
            self.mostrar_info(titulo, mensaje)

            

    def buscar_ruta_corta(self):
        start = self.start_var.get()
        end = self.end_var.get()
        tiene_visa = self.bool_var.get()

        if start == end:
            messagebox.showwarning("Advertencia", "El inicio y el fin son el mismo aeropuerto. No hay necesidad de búsqueda.")
            return

        
        print(tiene_visa)
        if tiene_visa == True:
            ruta_menos_escalas = busqueda_en_anchura(self.graph, start, end, tiene_visa)
        else:
            ruta_menos_escalas = busqueda_en_anchura(self.graph_aux, start, end, tiene_visa)
    
        if ruta_menos_escalas:
            cost, path = ruta_menos_escalas
            stops = count_stops(path)            
            titulo = "Ruta con menos escalas"
            mensaje = f"{path} con costo de ${cost}\nNúmero de escalas: {stops}"
            self.mostrar_info(titulo, mensaje)
            self.mostrar_grafo(path)  # Mostrar el grafo con la ruta resaltada

        else:
            titulo = "Visa Requerida"
            mensaje = "No se puede encontrar una ruta debido a restricciones de visa"
            self.mostrar_info(titulo, mensaje)
            
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
