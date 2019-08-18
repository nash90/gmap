import googlemaps
import time
import pandas as pd

from datetime import datetime
from config import settings

key = settings["api_key"]
q='smoke shop'

gmaps = googlemaps.Client(key=key)

fields = ['place_id','opening_hours','icon', 'formatted_address'] 
location = '34.110113, -117.715292'
locationbias= 'circle:2000000@34.110113, -117.715292'
radius = '20000' 
#place = gmaps.find_place(input="smoke shop", input_type="textquery",
#fields=fields, location_bias=locationbias)

formated_data = {
  "name": "",
  "address": "",
  "id": "",
  "rating":"",
  "type":"",
  "user_rating_total":""
}

def get_places(q="smoke shop", location='34.110113, -117.715292', radius='40000'):
  return gmaps.places(query=q, location=location, radius=radius)

def get_places_with_token(q="smoke shop", location='34.110113, -117.715292', radius='40000', token=''):
  return gmaps.places(query=q, location=location, radius=radius, page_token=token)

res = get_places(q,location,radius)
places = res["results"]

global token 
token = None
loop = 0
max_loop =4

if res["next_page_token"] != None:
  token = res["next_page_token"]


while token != None and loop < max_loop:
  time.sleep(2)
  print("executing get_places_with_token loop")
  res = get_places_with_token(q, location, radius, token)
  print("break 2")
  result = res["results"]
  if result != None and len(result) >1:
    places = places + res["results"]
  if "next_page_token" in res:
    token = res["next_page_token"]
  else:
    token = None
  loop = loop + 1

data = []
for item in places:
  obj = {
  "name": item["name"],
  "address": item["formatted_address"],
  "id": item["id"],
  "rating":item["rating"],
  "type":", ".join(item["types"]),
  "user_ratings_total":item["user_ratings_total"],
  "place_id":item["place_id"]
  } 
  data.append(obj)

df = pd.DataFrame(data)

df.to_csv("data.csv")
