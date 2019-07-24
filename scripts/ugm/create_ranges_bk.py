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

path = "data/list.xlsx"

df = pd.read_excel(path, sheet_name=0, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

map = {}


for j in range(1, r_count):
    book = int(df.iloc[j, 0])

    if book not in map:
        map[book] = {}

    books = map[book]

    page = df.iloc[j, 1]
    if not pd.isnull(page) and page != "":
        page = int(page)
        id = int(df.iloc[j, 2])

        books[page] = id



df = pd.read_excel(path, sheet_name=1, header=None, index_col=None)

r_count = len(df.index)
c_count = len(df.columns)

manifests = {}

for j in range(1, r_count):
    book = int(df.iloc[j, 0])
    manifest = df.iloc[j, 1]
    manifests[book] = manifest

sts = []

for book in manifests:
    books = map[book]
    manifest = manifests[book]

    res = urllib.request.urlopen(manifest)
    # json_loads() でPythonオブジェクトに変換
    manifest_data = json.loads(res.read().decode('utf-8'))

    canvases = manifest_data["sequences"][0]["canvases"]

    for page in books:
        canvas = canvases[page-1]
        canvas_id = canvas["@id"]

        st = {
            "@id" : manifest_data["@id"]+"#"+str(books[page]),
            "label": str(books[page]),
            "@type" : "sc:Range",
            "canvases" : [canvas_id]
        }
        sts.append(st)

manifest_data["structures"] = sts

fw2 = open("../../docs/kyushu/06.json", 'w')
json.dump(manifest_data, fw2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))