import os
from dotenv import load_dotenv

from googlemaps.client import Client
from googlemaps.directions import directions

# Google Maps Platform API_KEY
load_dotenv()
api_key = os.getenv("API_KEY")
print(f"Google Maps API_KEY: {api_key} {type(api_key)}\n")

# Configuração do client, origem e destino
client = Client(key=api_key)
origin = "Av. Eng. Eusébio Stevaux, 823 - Santo Amaro, São Paulo - SP, 04696-000"
destination = "Estádio Cícero Pompeu de Toledo - Morumbis"

# Obtendo rotas possíveis de origin -> destination
routes = directions(client, origin, destination)[0]['legs'][0]

# Dados obtidos
distance = routes['distance']['text']
duration = routes['duration']['text']
end_address = routes['end_address']
end_location = routes['end_location']
start_address = routes['start_address']
start_location = routes['start_location']
            

print(f"Distance: {distance}\n"
      f"Duration: {duration}\n"
      f"End Address: {end_address}\n"
      f"End Location (lat/lng): {end_location}\n"
      f"Start Eddress: {start_address}\n"
      f"Start Location (lat/lng): {start_location}\n")