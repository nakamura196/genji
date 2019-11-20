import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json
import urllib.request
import os
import csv
import glob
import requests

url = "https://www.dl.ndl.go.jp/api/iiif/3437686/manifest.json"
headers = {"content-type": "application/json"}
r = requests.get(url, headers=headers)
data = r.json()

rows = []
rows.append(["manifest", "member_id", "line_id"])

canvases = data["sequences"][0]["canvases"]

for page in range(5, 29):
    canvas_index = 20 + int(page / 2)
    canvas = canvases[canvas_index - 1]
    canvas_uri = canvas["@id"]
    half = canvas["width"] / 2
    if (page % 2 == 0):
        canvas_uri += "#xywh=" + str(half) + ",0," + str(half) + "," + str(canvas["height"]);
    else:
        canvas_uri += "#xywh=" + "0,0," + str(half) + "," + str(canvas["height"]);
    

    rows.append([url, canvas_uri, "https://w3id.org/kouigenjimonogatari/data/"+str(page).zfill(4)+"-01.json"])


import csv

f = open('curation_ndl.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()

