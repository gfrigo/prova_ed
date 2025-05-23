from typing import Dict
import heapq

def dijkstra(graph: Dict, start: str) -> Dict:
  min_heap = [(0, start)] # Início [(0, 'A')]
  distances = {node: float('inf') for node in graph}
  distances[start] = 0 # Distância 'A' conhecida

  while min_heap:
    current_distance, current_node = heapq.heappop(min_heap)

    if current_distance > distances[current_node]:
      continue

    for neighbor, weight in graph[current_node].items():
      distance = current_distance + weight

      if distance < distances[neighbor]:
        distances[neighbor] = distance
        heapq.heappush(min_heap, (distance, neighbor))
        0

  return distances

graph = {
    'A': {'B': 2, 'C': 4},
    'B': {'A': 2, 'C': 1, 'D': 7},
    'C': {'A': 4, 'B': 1, 'D': 2},
    'D': {'B': 7, 'C': 2, 'E': 2},
    'E': {'C': 10, 'D': 2},
}

start = 'A'

distances = dijkstra(graph, start)
print(distances)