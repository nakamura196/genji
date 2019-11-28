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

import csv

map = {}

label_map = {
    "https://nakamura196.github.io/genji/ugm/ndl/manifest/3437686.json": "校異源氏物語",
    "https://nakamura196.github.io/genji/ugm/utokyo/manifest/01.json": "東大本",
    "https://nakamura196.github.io/genji/ugm/kyushu/manifest/01.json": "九大本（古活字版）",
    "https://nakamura196.github.io/genji/ugm/kyushu2/manifest/01.json": "九大本（無跋無刊記整版本）"
}

with open('curation_merged.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        manifest = row[0]
        member_id = row[1]
        label = row[2]
        line_id = row[3]
        sort = row[4]
        if manifest not in map:
            map[manifest] = {}
        map[manifest][sort] = {
            "label": label,
            "line_id": line_id,
            "member_id": member_id
        }


selections = []
for manifest in map:

    members = []

    for sort in sorted(map[manifest]):
        obj = map[manifest][sort]

        member = {
            "@id": obj["member_id"],
            "@type": "sc:Canvas",
            "label": obj["label"]
        }

        members.append(member)

        if "line_id" in obj and obj["line_id"] != "":
            member["line_id"] = obj["line_id"]

    selection = {
        "@id": "http://mp.ex.nii.ac.jp/api/curation/json/9ab5cac5-78e6-41b8-9d8f-ab00f57d7b64/range1",
        "@type": "sc:Range",
        "label": "Manual curation by IIIF Curation Viewer",
        "members": members,
        "within": {
            "@id": manifest,
            "@type": "sc:Manifest",
            "label": label_map[manifest]
        }
    }

    selections.append(selection)

curation_data = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@type": "cr:Curation",
    "@id": "http://mp.ex.nii.ac.jp/api/curation/json/9ab5cac5-78e6-41b8-9d8f-ab00f57d7b64",
    "label": "Curating list",
    "selections": selections
}

fw2 = open("curation.json", 'w')
json.dump(curation_data, fw2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
