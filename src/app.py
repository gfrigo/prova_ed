import folium 
import polyline
import networkx as nx
import streamlit as st 
from folium import plugins
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

from maps import connect_api, get_directions, duration_to_minutes
from dijkstra import dijkstra

st.set_page_config(layout="centered") 
st.title("Algoritmo de Dijkstra")  
st.subheader("Alunos")
st.markdown("""
- Gabriel Frigo Sena Silva
- Felipe Cordeiro de Carvalho
""")

origins = ["R. José Fugulin, 233 - Vila Campo Grande", "R. Relva Velha, 46 - Jardim Sertaozinho", "R. Inocêncio de Camargo - Jardim Pedreira", "R. Olívia Guedes Penteado, 1160 - Socorro - SP, 04766-000", "R. Eugênio Pradez - Jardim Piracuama", "Av. Eng. Eusébio Stevaux, 823 - Santo Amaro, São Paulo - SP, 04696-000"]
destination = "Av. Eng. Eusébio Stevaux, 823 - Santo Amaro, São Paulo - SP, 04696-000"

client = connect_api()

graph = {}
routes_info = {}
coordinates = {}

nodes = origins + [destination]
for node in nodes:
    graph[node] = {}

G = nx.DiGraph()

st.info("Consultando rotas com a API... Isso pode levar alguns segundos.")

for i in range(len(origins)):
  for j in range(i + 1, len(origins)):
    a, b = origins[i], origins[j]

    # A -> B
    route_ab = get_directions(client, a, b)
    duration_ab = duration_to_minutes(route_ab["duration"])
    graph[a][b] = duration_ab
    G.add_edge(a, b, weight=duration_ab)

    routes_info[(a, b)] = route_ab

    if not coordinates.get(a):
      coordinates[a] = (route_ab['start_location']['lat'], route_ab['start_location']['lng'])
    if not coordinates.get(b):
      coordinates[b] = (route_ab['end_location']['lat'], route_ab['end_location']['lng'])

    # B -> A
    route_ba = get_directions(client, b, a)
    duration_ba = duration_to_minutes(route_ba["duration"])
    graph[b][a] = duration_ba
    G.add_edge(b, a, weight=duration_ba)

    routes_info[(b, a)] = route_ba

    if not coordinates.get(b):
      coordinates[b] = (route_ba['start_location']['lat'], route_ba['start_location']['lng'])
    if not coordinates.get(a):
      coordinates[a] = (route_ba['end_location']['lat'], route_ba['end_location']['lng'])

# Conecta cada origem ao destino
for origin in origins:
  route_to_dest = get_directions(client, origin, destination)
  duration_to_dest = duration_to_minutes(route_to_dest["duration"])
  graph[origin][destination] = duration_to_dest
  G.add_edge(origin, destination, weight=duration_to_dest)

  routes_info[(origin, destination)] = route_to_dest
  if not coordinates[origin]:
      coordinates[origin] = (route_to_dest['start_location']['lat'], route_to_dest['start_location']['lng'])
  if not coordinates[destination]:
      coordinates[destination] = (route_to_dest['end_location']['lat'], route_to_dest['end_location']['lng'])

st.subheader("Grafo de Endereços com Tempos de Trajeto")

fig, ax = plt.subplots(figsize=(14, 10)) 
pos = nx.spring_layout(G, seed=42) 

nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1200, node_color="lightblue")  
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", arrows=True, arrowsize=20) 
nx.draw_networkx_labels(G, pos, ax=ax, font_size=8) 

edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8) 

plt.axis("off") 
st.pyplot(fig) 

start = origins[-1]
distances = dijkstra(graph, start)

for node, conn in graph.items():
   print(f"Chave: {node} Valor: {conn}\n")

st.subheader("Mapa Interativo com Folium")

m = folium.Map(location=coordinates[destination], zoom_start=13)

for node, coord in coordinates.items():
    folium.Marker(
        location=coord,
        popup=node,
        tooltip=node,
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

shortest_paths = {}
for target_node in nodes:
    if target_node == start:
        continue
    path = []
    current = target_node
    while current != start:
        for prev_node, neighbors in graph.items():
            if current in neighbors:
                expected_time = distances[prev_node] + graph[prev_node][current]
                if expected_time == distances[current]:
                    path.insert(0, (prev_node, current))
                    current = prev_node
                    break
    shortest_paths[target_node] = path

shortest_edges = set()
for edge_list in shortest_paths.values():
    shortest_edges.update(edge_list)

for (origin, target), route_data in routes_info.items():
    encoded_polyline = route_data['polyline']
    decoded_points = polyline.decode(encoded_polyline)

    is_shortest = (origin, target) in shortest_edges
    color = 'blue' if is_shortest else 'red'

    folium.PolyLine(
        locations=decoded_points,
        color=color,
        weight=4 if is_shortest else 3,
        opacity=0.9 if is_shortest else 0.6,
        tooltip=f"{origin} → {target}"
    ).add_to(m)


plugins.MiniMap(toggle_display=True).add_to(m)

st_data = st_folium(m, width=1000, height=600)

st.subheader("Distâncias calculadas com Dijkstra (em minutos):")  
st.json(distances)