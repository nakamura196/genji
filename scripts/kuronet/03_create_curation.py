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

manifest = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/c1ea8e6b-9403-4394-8619-96aad0ec6329/manifest"

uuid = hashlib.md5(manifest.encode('utf-8')).hexdigest()

r = requests.get(manifest)
manifest_data = json.loads(r.content)

canvases = manifest_data["sequences"][0]["canvases"]

canvas_index = {}

for i in range(len(canvases)):
    canvas_index[canvases[i]["@id"]] = i


map = {}

with open('result.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        if row[0] == manifest:
            canvas = row[1]

            if canvas not in map:
                map[canvas_index[canvas]] = row[2]

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
    curation_uri = map[canvas]
    r = requests.get(curation_uri)
    curation_data = json.loads(r.content)
    members_ = curation_data["selections"][0]["members"]

    for member in members_:
        members.append(member)


opath = "../../docs/kuronet/"+uuid+".json"

fw = open(opath, 'w')
json.dump(curation, fw, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
