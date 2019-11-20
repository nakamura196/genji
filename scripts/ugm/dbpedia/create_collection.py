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
import requests

path = "wiki.xlsx"

rep = ["https://nakamura196.github.io/genji", "../../../docs"]

df = pd.read_excel(path, sheet_name=1, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

map = {}
lmap = {}

for j in range(3, r_count):
    manifest = df.iloc[j,0]
    label = df.iloc[j, 1]
    collection = df.iloc[j, 2]
    clabel = df.iloc[j, 3]
    index = df.iloc[j, 4]

    if collection not in map:
        map[collection] = []
        lmap[collection] = clabel

    obj = {
        "label": label,
        "@id": manifest
    }

    map[collection].append(obj)

    if not pd.isnull(index):
        obj["index"] = index

for collection_uri in map:

    opath = collection_uri.replace(rep[0], rep[1])

    if os.path.exists(opath):
        continue

    odir = os.path.split(opath)[0]
    os.makedirs(odir, exist_ok=True)

    collection = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": collection_uri,
        "@type": "sc:Collection",
        "label": lmap[collection_uri],
        "manifests": [],
        "vhint": "use-thumb"
    }

    for obj in map[collection_uri]:

        manifest_uri = obj["@id"]
        print(manifest_uri)

        r = requests.get(manifest_uri)
        data = r.json()

        thumbnail_uri = data["sequences"][0]["canvases"][0]["images"][0]["resource"]["service"]["@id"]+"/full/200,/0/default.jpg"

        manifest = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": manifest_uri,
            "@type": "sc:Manifest",
            "label": data["label"],
            "thumbnail": thumbnail_uri
        }
        if "index" in obj:
            manifest["index"] = obj["index"]

        collection["manifests"].append(manifest)


    fw2 = open(opath, 'w')
    json.dump(collection, fw2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
