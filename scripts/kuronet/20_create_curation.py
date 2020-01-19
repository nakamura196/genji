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


map = {}

with open('data/input.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        id = row[0]
        label = row[1]
        curation = row[2]

        if id not in map:
            map[id] = {
                "label": label,
                "members": []
            }

        map[id]["members"].append(curation)


for id in map:

    curation_uri = "https://nakamura196.github.io/genji/kuronet2/"+id+".json"

    members = []

    obj = map[id]

    curation = {
        "selections": [
            {
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

    curations = obj["members"]
    for i in range(len(curations)):
        curation_uri = curations[i]

        r = requests.get(curation_uri)
        curation_data = json.loads(r.content)
        members_ = curation_data["selections"][0]["members"]

        for member in members_:
            members.append(member)

        if i == 0:
            curation["selections"][0]["within"] = curation_data["selections"][0]["within"]

    opath = "../../docs/kuronet2/"+id+".json"

    fw = open(opath, 'w')
    json.dump(curation, fw, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
