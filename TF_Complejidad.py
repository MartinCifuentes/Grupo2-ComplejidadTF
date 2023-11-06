import pandas as pd
import heapq
import matplotlib.pyplot as plt
import math
def haversine_distance(lat1, lon1, lat2, lon2):
     R = 6371
     dlat = math.radians(lat2 - lat1)
     dlon = math.radians(lon2 - lon1)
     a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2))
     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
     d = R * c
     return d
archivo_xlsx = "Prueba grafo.xlsx"
df = pd.read_excel(archivo_xlsx)
# Crear un grafo como un diccionario de adyacencia
graph = {}
for i in range(len(df)):
     node1 = df.loc[i, 'Direcciones']
     graph[node1] = {}
     for j in range(i + 1, len(df)):
         node2 = df.loc[j, 'Direcciones']
         distancia = haversine_distance(df.loc[i, 'Latitude'], df.loc[i, 'Longitude'], df.loc[j, 'Latitude'], df.loc[j, 'Longitude'])
         graph[node1][node2] = distancia
         graph[node2] = {} # Agregar el nodo inverso

# Implementación de Dijkstra
def dijkstra(graph, start, end):
     distances = {node: float('inf') for node in graph}
     distances[start] = 0
     previous_nodes = {}
     nodes_to_visit = [(start, 0)]
     while nodes_to_visit:
         current_node, current_distance = heapq.heappop(nodes_to_visit)
         if current_distance > distances[current_node]:
            continue
         for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
         if distance < distances[neighbor]:
            distances[neighbor] = distance
            previous_nodes[neighbor] = current_node
            heapq.heappush(nodes_to_visit, (neighbor, distance))
     path = []
     while end:
        path.insert(0, end)
        end = previous_nodes.get(end)
     return path

origen = "Calle 4, Santiago de Surco, Provincia de Lima"
destino = "Calle 5, Santiago de Surco, Provincia de Lima"
ruta_minima_nodos = dijkstra(graph, origen, destino)
# Visualización del grafo y la ruta mínima
plt.figure(figsize=(18, 8)) # Ajustar el tamaño de la figura (ancho x  alto)

for node1 in graph:
    for node2, weight in graph[node1].items():
        lat1, lon1 = df.loc[df['Direcciones'] == node1, ['Latitude', 'Longitude']].values[0]
        lat2, lon2 = df.loc[df['Direcciones'] == node2, ['Latitude', 'Longitude']].values[0]
        plt.plot([lon1, lon2], [lat1, lat2], marker='o', markersize=4, color='gray',linestyle='dashed', alpha=0.5)

for i in range(len(ruta_minima_nodos) - 1):
     node1 = ruta_minima_nodos[i]
     node2 = ruta_minima_nodos[i + 1]
     lat1, lon1 = df.loc[df['Direcciones'] == node1, ['Latitude','Longitude']].values[0]
     lat2, lon2 = df.loc[df['Direcciones'] == node2, ['Latitude','Longitude']].values[0]
     # Agregar un pequeño espacio entre los nodos de la ruta mínima
     delta_lat = (lat2 - lat1) * 0.1
     delta_lon = (lon2 - lon1) * 0.1
     plt.plot([lon1, lon2], [lat1, lat2], marker='o', markersize=4, color='red', linestyle='solid', linewidth=3) # Aumentar el grosor

# Etiquetar las aristas con la distancia
for node1 in graph:
     for node2, weight in graph[node1].items():
        lat1, lon1 = df.loc[df['Direcciones'] == node1, ['Latitude', 'Longitude']].values[0]
        lat2, lon2 = df.loc[df['Direcciones'] == node2, ['Latitude', 'Longitude']].values[0]
        label_x = (lon1 + lon2) / 2
        label_y = (lat1 + lat2) / 2
        plt.text(label_x, label_y, f'{round(weight, 2)} km', fontsize=8, ha='center', va='center', color='black')

plt.scatter(df['Longitude'], df['Latitude'], s=100, color='lightblue',
edgecolor='black', zorder=2)
plt.title(f"Ruta Mínima de {origen} a {destino}")
plt.axis('off') # Desactivar ejes
plt.xticks([]) # Eliminar marcas de graduación en el eje x
plt.yticks([]) # Eliminar marcas de graduación en el eje y

# Guardar la figura en un archivo en lugar de mostrarla
plt.savefig("ruta_minima.png", bbox_inches='tight', pad_inches=0)
