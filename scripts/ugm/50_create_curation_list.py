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
rows.append(["manifest", "member_id", "line_id"])

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
                
                member_id = canvas+"#xywh="+area[0]+","+area[1]+","+area[2]+","+str(manifest_map[manifest][canvas])

                chars = r["resource"]["chars"]
                if "源氏物語大成" not in chars:
                    continue
                page = chars.split(" ")[1].split(".")[1]
                line_id = "https://w3id.org/kouigenjimonogatari/data/"+page.zfill(4)+"-01.json"
                # print(member_id)

                rows.append([manifest, member_id, line_id])


import csv

f = open('curation_list.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()

