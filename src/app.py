from maps import connect_api, get_directions, duration_to_minutes
from dijkstra import dijkstra

origins = ["R. José Fugulin, 233 - Vila Campo Grande", "R. Relva Velha, 46 - Jardim Sertaozinho", "R. Inocêncio de Camargo - Jardim Pedreira", "R. Olívia Guedes Penteado, 1160 - Socorro - SP, 04766-000", "R. Eugênio Pradez - Jardim Piracuama"]
destination = "Av. Eng. Eusébio Stevaux, 823 - Santo Amaro, São Paulo - SP, 04696-000"

client = connect_api()

graph = {}

nodes = origins + [destination]
for node in nodes:
    graph[node] = {}

for i in range(len(origins)):
  for j in range(i + 1, len(origins)):
    a, b = origins[i], origins[j]

    # A -> B
    route_ab = get_directions(client, a, b)
    duration_ab = duration_to_minutes(route_ab["duration"])
    graph[a][b] = duration_ab

    # B -> A
    route_ba = get_directions(client, b, a)
    duration_ba = duration_to_minutes(route_ba["duration"])
    graph[b][a] = duration_ba

# Conecta cada origem ao destino
for origin in origins:
  route_to_dest = get_directions(client, origin, destination)
  duration_to_dest = duration_to_minutes(route_to_dest["duration"])
  graph[origin][destination] = duration_to_dest

for node, conn in graph.items():
   print(f"Chave: {node} Valor: {conn}\n")