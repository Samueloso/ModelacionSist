# ui.py
import tkinter as tk
from tkinter import messagebox
from graph_utils import mostrar_grafo, airports
from dijkstra import dijkstra, count_stops
import matplotlib.pyplot as plt

class RouteFinderApp:
    def __init__(self, root, graph):
        self.root = root
        self.graph = graph
        self.root.title("Buscador de Rutas de Vuelos")

        # Ajustar el tamaño de la ventana
        self.root.geometry("600x400")
        self.centrar_ventana(600, 400)

        tk.Label(root, text="Aeropuerto de origen:").grid(row=0, column=0)
        self.start_var = tk.StringVar(root)
        self.start_var.set(airports[0])  # Valor por defecto
        self.start_menu = tk.OptionMenu(root, self.start_var, *airports)
        self.start_menu.grid(row=0, column=1)

        tk.Label(root, text="Aeropuerto de destino:").grid(row=1, column=0)
        self.end_var = tk.StringVar(root)
        self.end_var.set(airports[0])  # Valor por defecto
        self.end_menu = tk.OptionMenu(root, self.end_var, *airports)
        self.end_menu.grid(row=1, column=1)

        self.bool_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Tiene visa", variable=self.bool_var).grid(row=2, columnspan=2)

        tk.Button(root, text="Buscar Ruta", command=self.buscar_ruta).grid(row=3, columnspan=2)

        tk.Button(root, text="Mostrar Grafo", command=lambda: self.mostrar_grafo()).grid(row=5, columnspan=2)

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
        ventana_emergente.geometry('300x150')

    def buscar_ruta(self):
        start = self.start_var.get()
        end = self.end_var.get()
        tiene_visa = self.bool_var.get()
        
        if start not in self.graph or end not in self.graph:
            messagebox.showerror("Error", "Aeropuertos inválidos. Por favor ingrese aeropuertos válidos.")
            return
        
        if start == end:
            messagebox.showwarning("Advertencia", "El inicio y el fin son el mismo aeropuerto. No hay necesidad de búsqueda.")
            return

        ruta_mas_barata = dijkstra(self.graph, start, end, tiene_visa)
        
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
