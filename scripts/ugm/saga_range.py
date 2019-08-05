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

# 空の場合はすべて
target = ""

path = "data/all.json"

label_map = {}

top_dir = "../../docs/ugm/saga"

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

    if target != "" and dir != target:
        continue

    list_path = "data/"+dir+"/list_"+dir+".xlsx"

    df = pd.read_excel(list_path, sheet_name=1, header=None, index_col=None)

    r_count = len(df.index)
    c_count = len(df.columns)

    # curationリストの列がない場合
    if c_count < 4:
        continue

    manifests = {}

    for j in range(1, r_count):
        book = int(df.iloc[j, 0])
        manifest = df.iloc[j, 1]
        curation = df.iloc[j, 3]

        manifests[book] = {
            "manifest": manifest
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

        odir = top_dir + "/"+dir+"/manifest"
        os.makedirs(odir, exist_ok=True)

        ofile_1 = odir+"/"+str(book).zfill(2)+".json"

        new_manifest_uri = ofile_1.replace(
            "../../docs", "https://nakamura196.github.io/genji")

        # -------------- <curation> ---------------

        annodir = top_dir + "/"+dir+"/anno"
        os.makedirs(annodir, exist_ok=True)

        # sts = []  # 初期化します

        if "curation" in manifests[book]:
            curation_uri = manifests[book]["curation"]

            curation_data = requests.get(curation_uri).json()

            members = curation_data["selections"][0]["members"]

            canvas_anno_map = {}

            for member in members:
                cu_id = member["@id"].split("#")
                page = member["metadata"][0]["value"]

                canvas_id = cu_id[0]
                area = cu_id[1]
                canvas_index = c_index_map[canvas_id]

                print(canvas_index)

                # hash = hashlib.md5(canvas_id.encode('utf-8')).hexdigest()
                hash = "anno_"+str(canvas_index+1).zfill(3)+"_" + \
                    hashlib.md5(canvas_id.encode('utf-8')).hexdigest()

                anno_file = annodir+"/" + hash + ".json"

                anno_uri = anno_file.replace(
                    "../../docs", "https://nakamura196.github.io/genji")

                if canvas_index not in canvas_anno_map:
                    canvas_anno_map[canvas_index] = []

                areas = area.split("=")[1].split(",")

                x = str(int(areas[0])+int(int(areas[2]) / 2))
                y = areas[1]

                anno_id = anno_uri+"#"+str(len(canvas_anno_map[canvas_index]))

                anno = {
                    "@id": anno_id,
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "resource": {
                        "@type": "dctypes:Text",
                        "chars": "新編日本古典文学全集 p."+page+" 開始位置<p><a href=\"https://japanknowledge.com/lib/display/?lid=80110V00200"+page.zfill(3)+"\" target=\"_blank\" rel=\"noopener noreferrer\">ジャパンナレッジ</a>でみる</p>",
                        "format": "text/html"
                    },
                    "on": [
                        {
                            "@type": "oa:SpecificResource",
                            "full": canvas_id,
                            "selector": {
                                "@type": "oa:Choice",
                                "default": {
                                    "@type": "oa:FragmentSelector",
                                    "value": "xywh="+x+","+y+",90,135"
                                },
                                "item": {
                                    "@type": "oa:SvgSelector",
                                    "value": "<svg xmlns='http://www.w3.org/2000/svg'><path xmlns=\"http://www.w3.org/2000/svg\" d=\"M"+x+","+y+"c0,-30 15,-60 45,-90c0,-25 -20,-45 -45,-45c-25,0 -45,20 -45,45c30,30 45,60 45,90z\" id=\"pin_"+hashlib.md5(member["@id"].encode('utf-8')).hexdigest()+"\" fill=\"#F6E920\" stroke=\"#F6E920\"/></svg>"
                                }
                            },
                            "within": {
                                "@id": new_manifest_uri,
                                "@type": "sc:Manifest"
                            }
                        }
                    ],
                }

                canvas_anno_map[canvas_index].append(anno)

                '''

                fw2 = open(anno_file, 'w')
                json.dump(anno_data, fw2, ensure_ascii=False, indent=4,
                        sort_keys=True, separators=(',', ': '))

                canvases[canvas_index]["otherContent"] =  [
                    {
                        "@id": anno_uri,
                        "@type": "sc:AnnotationList"
                    }
                ]

                '''

            for canvas_index in canvas_anno_map:

                canvas_id = canvases[canvas_index]["@id"]

                # hash = hashlib.md5(canvas_id.encode('utf-8')).hexdigest()
                hash = "anno_"+str(canvas_index+1).zfill(3)+"_" + \
                    hashlib.md5(canvas_id.encode('utf-8')).hexdigest()

                anno_file = annodir+"/" + hash + ".json"

                anno_uri = anno_file.replace(
                    "../../docs", "https://nakamura196.github.io/genji")

                anno_data = {
                    "@context": "http://iiif.io/api/presentation/2/context.json",
                    "@id": anno_uri,
                    "@type": "sc:AnnotationList",
                    "resources": canvas_anno_map[canvas_index]
                }

                fw2 = open(anno_file, 'w')
                json.dump(anno_data, fw2, ensure_ascii=False, indent=4,
                          sort_keys=True, separators=(',', ': '))

                canvases[canvas_index]["otherContent"] = [
                    {
                        "@id": anno_uri,
                        "@type": "sc:AnnotationList"
                    }
                ]

        # manifest_data["structures"] = sts

        fw2 = open(ofile_1, 'w')
        json.dump(manifest_data, fw2, ensure_ascii=False, indent=4,
                  sort_keys=True, separators=(',', ': '))

        thumbnail = manifest_data["sequences"][0]["canvases"][0]["images"][0]["resource"]["service"]["@id"] + \
            "/full/200,/0/default.jpg"

        manifests4collection.append({
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": new_manifest_uri,
            "@type": "sc:Manifest",
            "label": label_map[book],
            "index": book,
            "thumbnail": thumbnail
        })

    ofile = top_dir + "/"+dir+"/collection.json"

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
