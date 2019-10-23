import googlemaps
import time
import pandas as pd

from datetime import datetime
from config import settings

key = settings["api_key"]
q='restaurant'

gmaps = googlemaps.Client(key=key)

fields = ['place_id','opening_hours','icon', 'formatted_address'] 
location = '34.110113, -117.715292'
#locationbias= 'circle:2000000@34.110113, -117.715292'
radius = '5000' 
#place = gmaps.find_place(input="smoke shop", input_type="textquery",
#fields=fields, location_bias=locationbias)
data = []
places = []
max_count = 2

cities_df = pd.read_csv("la_cities.csv")
cities_cords = {}

for index, row in cities_df.iterrows():
  city = row["city"]
  city_coordinate = str(row["lat"]) + ", " + str(row["lng"])
  cities_cords[city] = city_coordinate


formated_data = {
  "name": "",
  "address": "",
  "id": "",
  "rating":"",
  "type":"",
  "user_rating_total":""
}

def get_places(q="smoke shop", location='34.110113, -117.715292', radius='5000'):
  return gmaps.places(query=q, location=location, radius=radius)

def get_places_with_token(q="smoke shop", location='34.110113, -117.715292', radius='5000', token=''):
  return gmaps.places(query=q, location=location, radius=radius, page_token=token)

def get_places_for_location(q,location,radius, city_name = "none"):
  global data, places
  res = get_places(q,location,radius)
  places = res["results"]

  token = None

  if res["next_page_token"] != None:
    token = res["next_page_token"]

  count = 1
  while token != None and count < max_count:
    time.sleep(2)
    print("executing get_places_with_token loop: " + location)
    res = get_places_with_token(q, location, radius, token)
    #print("break 2")
    result = res["results"]
    if result != None and len(result) >1:
      places = places + res["results"]
    if "next_page_token" in res:
      token = res["next_page_token"]
    else:
      token = None
    count = count+1

  for item in places:
    obj = {
    "city": city_name,      
    "name": item["name"],
    "address": item["formatted_address"],
    "id": item["id"],
    "rating":item["rating"],
    "type":", ".join(item["types"]),
    "user_ratings_total":item["user_ratings_total"],
    "place_id":item["place_id"],
    "lattitude": item["geometry"]["location"]["lat"],
    "longitude": item["geometry"]["location"]["lng"]
    } 
    data.append(obj)



def save_csv():
  df = pd.DataFrame(data)

  df.to_csv("data.csv")

def run_script():
  #get_places_for_location(q,location,radius)

  for key, value in cities_cords.items():
    get_places_for_location(q, value, radius, key)
    #if key == "Avocado Heights":
      #break

  save_csv()

run_script()
