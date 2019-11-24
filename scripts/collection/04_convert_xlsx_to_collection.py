import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json
from urllib import request
from bs4 import BeautifulSoup
import hashlib
import os
import requests

path = "data/ほぼ揃い(50冊以上)源氏物語_NIJLrev.xlsx"

df = pd.read_excel(path, sheet_name="ほぼ揃い源氏", header=None, index_col=None)


r_count = len(df.index)
c_count = len(df.columns)

print(r_count)

collections = []

for j in range(1, r_count):
    url = str(df.iloc[j, 4])

    manifest = str(df.iloc[j, 6])
    print(manifest)

    try:

        headers = {"content-type": "application/json"}
        r = requests.get(manifest, headers=headers)
        data = r.json()

        type_ = "sc:Manifest"
        if "nakamura196" in manifest:
            type_ = "sc:Collection"

        collections.append(
            {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": manifest,
            "@type": type_,
            "label": data["label"],
            "attribution": str(df.iloc[j, 0]),
            "license": str(df.iloc[j, 5]),
            "type": str(df.iloc[j, 1]),
            "volume": str(df.iloc[j, 2]),
            "description": str(df.iloc[j, 3])
            }
        )
    except Exception as e:
        print(e)

collection_data = {
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": "https://nakamura196.github.io/genji/collections/top.json",
  "@type": "sc:Collection",
  "label": "IIIF対応源氏物語リスト",
  "collections": collections
}


with open("../../docs/collections/top.json", 'w') as f:
    json.dump(collection_data, f, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))
