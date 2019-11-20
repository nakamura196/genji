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

map = {}

top_uri = "http://ja.dbpedia.org/data/源氏物語.json"

uni = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": top_uri,
    "@type": "sc:Collection",
    "label": "源氏物語",
    "collections": [],
    "vhint": "use-thumb"
}

jmap = {
    top_uri: uni
}


def exec(parent):

    if parent not in map:
        return

    children = map[parent]

    j = jmap[parent]

    for child in children:
        if "collection" in child:
            collection_uri = child["collection"]
            collection = {
                "@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": collection_uri,
                "@type": "sc:Collection",
                "label": child["label"],
                "collections": [],
                "vhint": "use-thumb"
            }

            jmap[collection_uri] = collection
            j["collections"].append(collection)
            exec(collection_uri)
        else:
            manifest_uri = child["manifest"]

            if "manifests" not in j:
                j["manifests"] = []

            r = requests.get(manifest_uri)
            data = r.json()

            thumbnail_uri = data["sequences"][0]["canvases"][0]["images"][0]["resource"]["service"]["@id"] + \
                "/full/200,/0/default.jpg"

            j["manifests"].append({
                "@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": manifest_uri,
                "@type": "sc:Manifest",
                "label": child["label"],
                "thumbnail": thumbnail_uri
            })


path = "wiki.xlsx"

rep = ["https://nakamura196.github.io/genji", "../../../docs"]

df = pd.read_excel(path, sheet_name=0, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)


for j in range(3, r_count):
    collection = df.iloc[j, 0]
    manifest = df.iloc[j, 1]
    child = df.iloc[j, 2]
    label = df.iloc[j, 3]
    parent = df.iloc[j, 4]

    if not pd.isnull(parent) or parent == top_uri:

        if parent not in map:
            map[parent] = []

        if not pd.isnull(manifest) and manifest != 0:
            map[parent].append({
                "manifest": manifest,
                "label": label
            })

        if not pd.isnull(collection) and collection != 0:
            map[parent].append({
                "collection": collection,
                "label": label
            })

        if not pd.isnull(child) and child != 0:
            map[parent].append({
                "collection": child,
                "label": label
            })

exec(top_uri)

fw2 = open("../../../docs/ugm/genji.json", 'w')
json.dump(uni, fw2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
