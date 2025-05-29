import os
from dotenv import load_dotenv

from googlemaps.client import Client
from googlemaps.directions import directions


def connect_api():
  # Google Maps Platform API_KEY
  load_dotenv()
  api_key = os.getenv("API_KEY")
  print(f"Google Maps API_KEY: {api_key} {type(api_key)}\n")

  # Configuração do client, origem e destino
  return Client(key=api_key) 

def get_directions(client, origin:str, destination:str):
  # Obtendo rotas possíveis de origin -> destination
  route = directions(client, origin, destination)[0]["legs"][0]

  # Dados obtidos
  distance = route['distance']['text']
  duration = route['duration']['text']
  end_address = route['end_address']
  end_location = route['end_location']
  start_address = route['start_address']
  start_location = route['start_location']

  print(f"Distance: {distance}\n"
        f"Duration: {duration}\n"
        f"End Address: {end_address}\n"
        f"End Location (lat/lng): {end_location}\n"
        f"Start Eddress: {start_address}\n"
        f"Start Location (lat/lng): {start_location}\n")
  
  return {"route":route,
          "distance":distance,
          "duration":duration,
          "end_address":end_address,
          "end_location":end_location,
          "start_address":start_address,
          "start_location":start_location
          }

def duration_to_minutes(duration_text: str) -> int: # "7 hours 22 mins"
  # Ex: "1 hour 10 mins" ou "45 mins"
  duration_text = duration_text.lower()
  minutes = 0 
  parts = ""

  # Verifica se tem horas presentes no trajeto
  if 'hour' in duration_text:
    parts = duration_text.split('hour')
    hours = int(parts[0].strip())
    minutes += hours * 60

  # Verifica se ainda tem minutos depois das horas
  if len(parts) > 1 and 'min' in parts[1]:
    mins = int(parts[1].split('min')[0].strip())
    minutes += mins

  # Verifica se o trajeto demorará somente minutos
  if 'min' in duration_text:
    minutes = int(duration_text.split('min')[0].strip())

  return minutes