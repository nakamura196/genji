import json
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import os
import glob
from lxml import etree
import sys
import requests
import hashlib
import difflib
import time

import csv

end_curation_="https://mp.ex.nii.ac.jp/api/kuronet/curation/fb60af58ce5f28e27d281b566f9c4f48e03521cb"

'''
uuid = hashlib.md5(manifest.encode('utf-8')).hexdigest()

r = requests.get(manifest)
manifest_data = json.loads(r.content)

canvases = manifest_data["sequences"][0]["canvases"]

canvas_index = {}

for i in range(len(canvases)):
    canvas_index[canvases[i]["@id"]] = i

'''

m_map = {}

with open('result.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        manifest_ = row[0]
        canvas = row[1]
        curation = row[2]

        if curation == end_curation_:
            break

        if manifest_ not in m_map:
            m_map[manifest_] ={}

        map = m_map[manifest_]

        if canvas not in map:
            map[canvas] = []

        map[canvas].append(curation)

# print(m_map)



for manifest in m_map:

    uuid = hashlib.md5(manifest.encode('utf-8')).hexdigest()

    curation_uri = "https://nakamura196.github.io/genji/kuronet/"+uuid+".json"

    members = []

    r = requests.get(manifest)
    manifest_data = json.loads(r.content)

    label = manifest_data["label"]

    curation = {
        "selections": [
            {
                "within": {
                    "@type": "sc:Manifest",
                    "@id": manifest,
                    "label": label
                },
                "@id": curation_uri+"/range1",
                "label": "Characters",
                "members": members,
                "@type": "sc:Range"
            }
        ],
        "@id": curation_uri,
        "@type": "cr:Curation",
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "label": "Character List",
        "viewingHint": "annotation"
    }

    map = m_map[manifest]

    for canvas in sorted(map):

        # print(canvas)

        curations = map[canvas]

        for curation_uri in curations:

            r = requests.get(curation_uri)
            curation_data = json.loads(r.content)
            members_ = curation_data["selections"][0]["members"]

            for member in members_:
                members.append(member)


    opath = "../../docs/kuronet/"+uuid+".json"

    fw = open(opath, 'w')
    json.dump(curation, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    print(manifest+"\t"+uuid+"\t"+label)

'''

for manifest in m_map:

    uuid = hashlib.md5(manifest.encode('utf-8')).hexdigest()

    members = []

    curation_uri = "https://nakamura196.github.io/genji/kuronet/"+uuid+".json"

    curation = {
        "selections": [
            {
                "within": {
                    "@type": "sc:Manifest",
                    "@id": manifest,
                    "label": manifest_data["label"]
                },
                "@id": curation_uri+"/range1",
                "label": "Characters",
                "members": members,
                "@type": "sc:Range"
            }
        ],
        "@id": curation_uri,
        "@type": "cr:Curation",
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "label": "Character List",
        "viewingHint": "annotation"
    }

    for canvas in sorted(map):

        print(canvas)

        curations = map[canvas]

        for curation_uri in curations:

            r = requests.get(curation_uri)
            curation_data = json.loads(r.content)
            members_ = curation_data["selections"][0]["members"]

            for member in members_:
                members.append(member)


    opath = "../../docs/kuronet/"+uuid+".json"

    fw = open(opath, 'w')
    json.dump(curation, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

'''