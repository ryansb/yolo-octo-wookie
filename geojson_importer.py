#!/bin/python
import json
import pymongo

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.newdaters
#geojsons = [f for f in os.listdir('./daterbits') if f.endswith('shp.geojson')]
import sys
print sys.argv[1]
with open(sys.argv[1], 'r') as dajson:
    daters = json.loads(dajson.read())
    coll = db[sys.argv[1].split(".")[0].split("/")[1]]
    for place in daters['features']:
        coll.insert(place)
