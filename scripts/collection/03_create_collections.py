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

for j in range(1, r_count):
    url = str(df.iloc[j, 4])
    if "ndl" in url:

        collection_id = hashlib.md5(url.encode('utf-8')).hexdigest()

        collection_uri = "https://nakamura196.github.io/genji/collections/" + \
            collection_id+"/top.json"

        html = request.urlopen(url)

        # set BueatifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # get headlines
        aas = soup.find_all("a", attrs={"class", "ndltree-item"})

        collection_label = aas[0].text.split(" ")[0]

        manifests = []

        for i in range(1, len(aas)):
            a = aas[i]
            manifest = "https://www.dl.ndl.go.jp/api/iiif/" + \
                a.get("href").split("pid/")[1].split("?")[0] + "/manifest.json"

            print(manifest)

            label = a.text.split(" ")[0]

            headers = {"content-type": "application/json"}
            r = requests.get(manifest, headers=headers)
            data = r.json()

            manifests.append({
                "@context": "http://iiif.io/api/presentation/2/context.json",
                "@id": manifest,
                "@type": "sc:Manifest",
                "label": label,
                "thumbnail": data["sequences"][0]["canvases"][0]["thumbnail"]["@id"],
                "attribution": "国立国会図書館 National Diet Library, JAPAN",
                "license": "http://dl.ndl.go.jp/ja/iiif_license.html"
            })

        collection_data = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": collection_uri,
            "@type": "sc:Collection",
            "label": collection_label,
            "manifests": manifests
        }

        odir = "../../docs/collections/"+collection_id

        if not os.path.exists(odir):
            os.makedirs(odir, exist_ok=True)

        with open(odir+"/top.json", 'w') as f:
            json.dump(collection_data, f, ensure_ascii=False, indent=4,
                      sort_keys=True, separators=(',', ': '))
