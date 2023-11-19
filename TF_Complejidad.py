import pandas as pd
import heapq
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import ttk

def haversine_distance(lat1, lon1, lat2, lon2):
     R = 6371
     dlat = math.radians(lat2 - lat1)
     dlon = math.radians(lon2 - lon1)
     a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2))
     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
     d = R * c
     return d

# Implementación de Dijkstra
def dijkstra(graph, start, end, avoid_street=None):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {}
    nodes_to_visit = [(start, 0)]

    while nodes_to_visit:
        current_node, current_distance = heapq.heappop(nodes_to_visit)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            if avoid_street and (current_node == avoid_street or neighbor == avoid_street):
                continue
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(nodes_to_visit, (neighbor, distance))

    # Construir el camino
    path = []
    while end:
        path.insert(0, end)
        end = previous_nodes.get(end)

    return path

def visualize_graph(graph, ruta_minima_nodos):
    common_suffix = ', Santiago de Surco, Provincia de Lima'
    
    for i in range(len(ruta_minima_nodos) - 1):
        node1 = ruta_minima_nodos[i]
        node2 = ruta_minima_nodos[i + 1]
        
        node_name1 = node1.replace(common_suffix, '')
        lat1, lon1 = df.loc[df['Direcciones'] == node1, ['Latitude', 'Longitude']].values[0]
        plt.scatter(lon1, lat1, color='blue')  # Nodo actual en azul
        plt.text(lon1, lat1, node_name1, fontsize=8, ha='right', va='bottom')

        node_name2 = node2.replace(common_suffix, '')
        lat2, lon2 = df.loc[df['Direcciones'] == node2, ['Latitude', 'Longitude']].values[0]
        plt.scatter(lon2, lat2, color='blue')  # Nodo vecino en azul
        plt.text(lon2, lat2, node_name2, fontsize=8, ha='right', va='bottom')

        # Dibujar línea entre nodos
        plt.plot([lon1, lon2], [lat1, lat2], color='gray', linestyle='dashed', linewidth=2)

        # Calcular la distancia entre nodos y agregarla como etiqueta
        distance = graph[node1][node2]
        label_x = (lon1 + lon2) / 2
        label_y = (lat1 + lat2) / 2
        plt.text(label_x, label_y, f'{round(distance, 2)} km', fontsize=8, ha='center', va='center', color='black')

    plt.axis('off')
    plt.xticks([])  
    plt.yticks([])  
    plt.show()

def on_calculate_route():
    origen = combo_origen.get()
    destino = combo_destino.get()
    avoid_street = combo_avoid.get()

    ruta_minima_nodos = dijkstra(graph, origen, destino, avoid_street)
    filtered_graph = {node: graph[node] for node in ruta_minima_nodos}
    
    distancia_total = 0
    for i in range(len(ruta_minima_nodos) - 1):
        node1 = ruta_minima_nodos[i]
        node2 = ruta_minima_nodos[i + 1]
        distancia_total += graph[node1][node2]
    
    ruta_str = " -> ".join(node.replace(", Santiago de Surco, Provincia de Lima", "") for node in ruta_minima_nodos)

    # Limpiar el área de visualización
    for widget in frame_visualizacion.winfo_children():
        widget.destroy()
    
    label_resultado.config(text=f"Ruta: {ruta_str} - Distancia Total: {round(distancia_total, 2)} km")
    visualize_graph(graph, ruta_minima_nodos)

# Cargar tus datos y construir el grafo
archivo_xlsx = "Prueba grafo.xlsx"
df = pd.read_excel(archivo_xlsx)

distancia_maxima = 1

# Crear un grafo como un diccionario de adyacencia
graph = {}
for i in range(len(df)):
    node1 = df.loc[i, 'Direcciones']
    graph[node1] = {}
    for j in range(i + 1, len(df)):
        node2 = df.loc[j, 'Direcciones']
        distancia = haversine_distance(df.loc[i, 'Latitude'], df.loc[i, 'Longitude'],
                                      df.loc[j, 'Latitude'], df.loc[j, 'Longitude'])
        if distancia <= distancia_maxima:
            graph[node1][node2] = distancia
            
# Asegurarse de que las conexiones sean bidireccionales
for node1 in graph:
    for node2, distance in graph[node1].items():
        # Verificar si la conexión en la dirección opuesta no existe y la distancia es menor a 1 km
        if node1 not in graph[node2] and distance <= distancia_maxima:
            # Agregar la conexión bidireccional
            graph[node2][node1] = distance

# Crear una interfaz gráfica
root = tk.Tk()
root.title("Ruta Mínima")

# Obtener dimensiones de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Configurar tamaño y posición para que la interfaz ocupe toda la pantalla
root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")

# Crear y configurar la interfaz
frame = ttk.Frame(root, padding="10", style='TFrame')
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_origen = ttk.Label(frame, text="Dirección de origen:")
label_origen.grid(column=1, row=1, sticky=tk.W)

# Crear el cuadro de texto para el origen con autocompletado
combo_origen = ttk.Combobox(frame, values=df['Direcciones'].tolist(), width=47)
combo_origen.grid(column=2, row=1, sticky=tk.W)
combo_origen.set('')  # Establecer el valor inicial

label_destino = ttk.Label(frame, text="Dirección de destino:")
label_destino.grid(column=1, row=3, sticky=tk.W)

# Crear el cuadro de texto para el destino con autocompletado
combo_destino = ttk.Combobox(frame, values=df['Direcciones'].tolist(), width=47)
combo_destino.grid(column=2, row=3, sticky=tk.W)
combo_destino.set('')  # Establecer el valor inicial como vacío

label_avoid_street = ttk.Label(frame, text="Evitar calle (opcional):")
label_avoid_street.grid(column=1, row=5, sticky=tk.W)

combo_avoid = ttk.Combobox(frame, values=df['Direcciones'].tolist(), width=47)
combo_avoid.grid(column=2, row=5, sticky=tk.W)
combo_avoid.set('')

button_calculate = ttk.Button(frame, text="Calcular Ruta", command=on_calculate_route)
button_calculate.grid(column=2, row=7, columnspan=2)

frame_visualizacion = ttk.Frame(root, padding="10", style='TFrame')
frame_visualizacion.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))

label_resultado = ttk.Label(frame, text="")
label_resultado.grid(column=0, row=8, columnspan=2) 

# Ejecutar la interfaz
root.mainloop()