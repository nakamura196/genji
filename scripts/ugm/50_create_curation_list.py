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

manifest_map = {}

def get_manifest_data(manifest):
    headers = {"content-type": "application/json"}
    r = requests.get(manifest, headers=headers)
    data = r.json()

    manifest_map[manifest] = {}

    canvases = data["sequences"][0]["canvases"]
    for canvas in canvases:
        manifest_map[manifest][canvas["@id"]] = canvas["height"]


path = "data/all.json"

ofile_2 = "../../docs/ugm/genji.json"

collections = []

with open(path, 'r') as f:
    data = json.load(f)

# print(data)

rows = []
rows.append(["manifest", "member_id", "label", "line_id", "sort"])

for obj in data:

    label2 = obj["label"]
    # print(label2)
    dir = obj["id"]

    print(dir)

    anno_dir = "../../docs/ugm/"+dir+"/anno"

    files = glob.glob(anno_dir+"/*.json")

    for file in files:
        with open(file, 'r') as f:
            anno_data = json.load(f)
            resources = anno_data["resources"]
            for r in resources:
                canvas = r["on"][0]["full"]
                area = r["on"][0]["selector"]["default"]["value"].split("=")[1].split(",")
                
                manifest = r["on"][0]["within"]["@id"]

                if manifest not in manifest_map:
                    get_manifest_data(manifest)
                
                member_id = canvas+"#xywh="+area[0]+","+area[1]+","+area[2]+","+str(manifest_map[manifest][canvas] - int(area[1]))

                chars = r["resource"]["chars"]
                page = chars.split(" ")[1].split(".")[1]

                if "源氏物語大成" not in chars:
                    line_id = ""
                    label = "新編日本古典文学全集 p."+str(page)
                else:
                    line_id = "https://w3id.org/kouigenjimonogatari/data/"+page.zfill(4)+"-01.json"
                    label = "源氏物語大成 p."+str(page)

                sort = str(page).zfill(5)+"-"+area[0].zfill(5)

                rows.append([manifest, member_id, label, line_id, sort])
                


import csv

f = open('curation_list.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()

