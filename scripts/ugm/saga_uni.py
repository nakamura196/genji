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

path = "data/all.json"

ofile_2 = "../../docs/ugm3/genji.json"

collections = []

with open(path, 'r') as f:
    data = json.load(f)

# print(data)

for obj in data:

    label2 = obj["label"]
    # print(label2)
    dir = obj["id"]

    ofile = "../../docs/ugm3/"+dir+"/collection.json"

    if not os.path.exists(ofile):
        continue

    # print(ofile)

    with open(ofile, 'r') as f2:
        collection_data = json.load(f2)

        # print(collection_data)

        collections.append({
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": collection_data["@id"],
            "@type": "sc:Collection",
            "label": label2,
        })

universe = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": ofile_2.replace("../../docs", "https://nakamura196.github.io/genji"),
    "@type": "sc:Collection",
    "label": "源氏物語IIIFコレクション",
    "collections": collections
}

fw2 = open(ofile_2, 'w')
json.dump(universe, fw2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
