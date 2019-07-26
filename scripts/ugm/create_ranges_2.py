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
import hashlib

target = "utokyo"

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

    '''

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

    '''

    df = pd.read_excel(list_path, sheet_name=1, header=None, index_col=None)

    r_count = len(df.index)
    c_count = len(df.columns)

    manifests = {}

    for j in range(1, r_count):
        book = int(df.iloc[j, 0])
        manifest = df.iloc[j, 1]
        curation = df.iloc[j, 2]

        manifests[book] = {
            "manifest" : manifest
        }

        if not pd.isnull(curation):
            manifests[book]["curation"] = curation

    manifests4collection = []

    # print(manifests)

    for book in manifests:

        print(label2+" book\t"+str(book))
        
        manifest = manifests[book]["manifest"]

        if pd.isnull(manifest):
            continue

        res = urllib.request.urlopen(manifest)
        # json_loads() でPythonオブジェクトに変換
        manifest_data = json.loads(res.read().decode('utf-8'))

        canvases = manifest_data["sequences"][0]["canvases"]
        c_index_map = {}
        for i in range(len(canvases)):
            c_index_map[canvases[i]["@id"]] = i

        # -------------- <mmm> ---------------

        odir = "../../docs/ugm2/"+dir+"/manifest"
        os.makedirs(odir, exist_ok=True)

        ofile_1 = odir+"/"+str(book).zfill(2)+".json"

        new_manifest_uri = ofile_1.replace(
            "../../docs", "https://nakamura196.github.io/genji")

        # -------------- <curation> ---------------

        annodir = "../../docs/ugm2/"+dir+"/anno"

        # sts = []  # 初期化します

        if "curation" in manifests[book]:
            curation_uri = manifests[book]["curation"]

            curation_data = requests.get(curation_uri).json()

            members = curation_data["selections"][0]["members"]

            for member in members:
                cu_id = member["@id"].split("#")
                page = member["metadata"][0]["value"]

                canvas_id = cu_id[0]
                area = cu_id[1]
                canvas_index = c_index_map[canvas_id]

                print(canvas_index)

                '''

                st = {
                    "@id": manifest_data["@id"]+"#"+str(canvas_index+1),
                    "label": str(page),
                    "@type": "sc:Range",
                    "canvases": [canvas_id]
                }
                sts.append(st)

                '''

                hash = hashlib.md5(canvas_id.encode('utf-8')).hexdigest()

                anno_file = annodir+"/" + hash + ".json"

                anno_uri = anno_file.replace(
                    "../../docs", "https://nakamura196.github.io/genji")

                anno_data = {
                    "@context": "http://iiif.io/api/presentation/2/context.json",
                    "@id": anno_uri,
                    "@type": "sc:AnnotationList",
                    "resources": [
                        {
                            "@id": anno_uri+"#0",
                            "@type": "oa:Annotation",
                            "motivation": "sc:painting",
                            "resource": {
                                "@type": "cnt:ContentAsText",
                                "chars": page,
                                "format": "text/plain"
                            },
                            "on": member["@id"]
                        }
                    ],
                    "within" : {
                        "@id" : new_manifest_uri,
                        "@type": "sc:Manifest"
                    }
                }

                fw2 = open(anno_file, 'w')
                json.dump(anno_data, fw2, ensure_ascii=False, indent=4,
                        sort_keys=True, separators=(',', ': '))

                canvases[canvas_index]["otherContent"] =  [
                    {
                        "@id": anno_uri,
                        "@type": "sc:AnnotationList"
                    }
                ]

        # manifest_data["structures"] = sts

        

        fw2 = open(ofile_1, 'w')
        json.dump(manifest_data, fw2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))

        thumbnail = manifest_data["sequences"][0]["canvases"][0]["images"][0]["resource"]["service"]["@id"]+"/full/200,/0/default.jpg"

        manifests4collection.append({
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": new_manifest_uri,
            "@type": "sc:Manifest",
            "label": label_map[book],
            "index": book,
            "thumbnail": thumbnail
        })

    ofile = "../../docs/ugm2/"+dir+"/collection.json"

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

