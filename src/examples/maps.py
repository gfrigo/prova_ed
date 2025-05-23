import os
from dotenv import load_dotenv

from googlemaps.client import Client
from googlemaps.directions import directions

# Google Maps Platform API_KEY
load_dotenv()
api_key = os.getenv("API_KEY")
print(f"Google Maps API_KEY: {api_key} {type(api_key)}")

client = Client(key=api_key)
origin = "Av. Eng. Eusébio Stevaux, 823 - Santo Amaro, São Paulo - SP, 04696-000"
destination = "Estádio Cícero Pompeu de Toledo - Morumbis"

routes = directions(client, origin, destination)
print(routes)