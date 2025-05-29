import networkx as nx
import streamlit as st 
import matplotlib.pyplot as plt

from maps import connect_api, get_directions, duration_to_minutes
from dijkstra import dijkstra

st.set_page_config(layout="wide") 
st.title("Visualização de Grafo com Algoritmo de Dijkstra")  

origins = ["R. José Fugulin, 233 - Vila Campo Grande", "R. Relva Velha, 46 - Jardim Sertaozinho", "R. Inocêncio de Camargo - Jardim Pedreira", "R. Olívia Guedes Penteado, 1160 - Socorro - SP, 04766-000", "R. Eugênio Pradez - Jardim Piracuama", "Av. Eng. Eusébio Stevaux, 823 - Santo Amaro, São Paulo - SP, 04696-000"]
destination = "Av. Eng. Eusébio Stevaux, 823 - Santo Amaro, São Paulo - SP, 04696-000"

client = connect_api()

graph = {}

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

    # B -> A
    route_ba = get_directions(client, b, a)
    duration_ba = duration_to_minutes(route_ba["duration"])
    graph[b][a] = duration_ba
    G.add_edge(b, a, weight=duration_ba)

# Conecta cada origem ao destino
for origin in origins:
  route_to_dest = get_directions(client, origin, destination)
  duration_to_dest = duration_to_minutes(route_to_dest["duration"])
  graph[origin][destination] = duration_to_dest
  G.add_edge(origin, destination, weight=duration_to_dest)

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

st.subheader("Distâncias calculadas com Dijkstra (em minutos):")  
start = origins[-1]
distances = dijkstra(graph, start)
st.json(distances)

for node, conn in graph.items():
   print(f"Chave: {node} Valor: {conn}\n")

start = origins[-1]
distances = dijkstra(graph, start)
print(distances)