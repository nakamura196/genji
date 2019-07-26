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

target = "kyushu"

path = "data/all.json"

label_map = {}

with open('data/map.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        label_map[int(row[0])] = row[1]


with open(path, 'r') as f:
    data = json.load(f)

for obj in data:

    label2 = obj["label"]
    # print(label2)
    dir = obj["id"]

    if dir != target:
        continue

    list_path = "data/"+dir+"/list_"+dir+".xlsx"

    df = pd.read_excel(list_path, sheet_name=0, header=None, index_col=None)

    r_count = len(df.index)
    c_count = len(df.columns)

    book_page_id_map = {}

    for j in range(1, r_count):

        cell = df.iloc[j, 0]

        if pd.isnull(cell) or cell == "":
            continue

        book = int(cell)

        if book not in book_page_id_map:
            book_page_id_map[book] = {}

        books = book_page_id_map[book]

        page = df.iloc[j, 1]
        if not pd.isnull(page) and page != "":
            page = int(page)
            id = int(df.iloc[j, 2])

            books[page] = id

    # print(book_page_id_map)

    df = pd.read_excel(list_path, sheet_name=1, header=None, index_col=None)

    r_count = len(df.index)
    c_count = len(df.columns)

    manifests = {}

    for j in range(1, r_count):
        book = int(df.iloc[j, 0])
        manifest = df.iloc[j, 1]
        manifests[book] = manifest    

    manifests4collection = []

    # print(manifests)

    for book in manifests:

        print(label2+" book\t"+str(book))
        
        manifest = manifests[book]

        if pd.isnull(manifest):
            continue

        res = urllib.request.urlopen(manifest)
        # json_loads() でPythonオブジェクトに変換
        manifest_data = json.loads(res.read().decode('utf-8'))

        canvases = manifest_data["sequences"][0]["canvases"]

        # -------------- <st> ---------------------

        sts = [] # 初期化します

        if book in book_page_id_map:
            books = book_page_id_map[book]

            for page in books:

                # print("page\t"+str(page))

                canvas = canvases[page-1]
                canvas_id = canvas["@id"]

                st = {
                    "@id": manifest_data["@id"]+"#"+str(books[page]),
                    "label": str(books[page]),
                    "@type": "sc:Range",
                    "canvases": [canvas_id]
                }
                sts.append(st)

        manifest_data["structures"] = sts

        # -------------- </st> ---------------------

        odir = "../../docs/ugm/"+dir+"/manifest"
        os.makedirs(odir, exist_ok=True)

        ofile_1 = odir+"/"+str(book).zfill(2)+".json"

        fw2 = open(ofile_1, 'w')
        json.dump(manifest_data, fw2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))

        thumbnail = manifest_data["sequences"][0]["canvases"][0]["images"][0]["resource"]["service"]["@id"]+"/full/200,/0/default.jpg"

        manifests4collection.append({
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": ofile_1.replace("../../docs", "https://nakamura196.github.io/genji"),
            "@type": "sc:Manifest",
            "label": label_map[book],
            "index": book,
            "thumbnail": thumbnail
        })

    ofile = "../../docs/ugm/"+dir+"/collection.json"

    collection_data = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": ofile.replace("../../docs", "https://nakamura196.github.io/genji"),
        "@type": "sc:Collection",
        "label": label2,
        "vhint": "use-thumb",
        "manifests": manifests4collection
    }

    fw2 = open(ofile, 'w')
    json.dump(collection_data, fw2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))

