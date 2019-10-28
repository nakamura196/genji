import urllib.request  # ライブラリを取り込む
import csv
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

import csv

reps = ["https://nakamura196.github.io/genji", "../../docs"]

map = {}

with open('data/images.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        id = row[0]
        if id not in map:
            map[id] = []

        map[id].append({
            "img": row[1],
            "thumb": row[2]
        })

f = open('data/config.json', 'r')
config_dict = json.load(f)

for config in config_dict:

    canvases = []

    manifest_uri = config["manifest_uri"]

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": config["manifest_uri"],
        "@type": "sc:Manifest",
        "label": config["label"],
        # "thumbnail": "https://iiif.dl.itc.u-tokyo.ac.jp/repo/files/medium/082f3475f5b03e1820688882d003ce39772ebb4c.jpg",
        # "license": "https://www.lib.u-tokyo.ac.jp/ja/library/contents/archives-top/reuse",
        # "logo": "https://iiif.dl.itc.u-tokyo.ac.jp/images/ut-logo.jpg",
        # "related": "https://iiif.dl.itc.u-tokyo.ac.jp/repo/s/genji/document/c1ea8e6b-9403-4394-8619-96aad0ec6329",
        # "seeAlso": "https://iiif.dl.itc.u-tokyo.ac.jp/repo/api/items/275151",
        # "within": "https://iiif.dl.itc.u-tokyo.ac.jp/repo/s/genji/",
        "sequences": [
            {
                "@id": manifest_uri+"/sequence/normal",
                "@type": "sc:Sequence",
                "label": "Current Page Order",
                "viewingHint": "non-paged",
                "canvases": canvases
            }
        ]
    }

    imgs = map[config["id"]]
    for i in range(len(imgs)):

        img_obj = imgs[i]

        if i == 0:
            manifest["thumbnail"] = {
                "@id": img_obj["thumb"]
            }

        canvas = {
            "@id": manifest_uri+"/canvas/p"+str(i+1),
            "@type": "sc:Canvas",
            "label": "["+str(i+1)+"]",
            "thumbnail": {
                "@id": img_obj["thumb"]
            },
            "width": 6642,
            "height": 4990,
            "images": [
                {
                    "@id": manifest_uri+"/annotation/p"+str(i).zfill(4)+"-image",
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "resource": {
                        "@type": "dctypes:Image",
                        "width": 6642,
                        "height": 4990,
                        "label": "オリジナル写真",
                        "format": "image/jpeg",
                        "@id": img_obj["thumb"]  # img_obj["img"]
                    },
                    "on": manifest_uri+"/canvas/p"+str(i+1)
                }
            ]
        }

        canvases.append(canvas)

    fw2 = open(manifest_uri.replace(reps[0], reps[1]), 'w')
    json.dump(manifest, fw2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))


'''

"@type": "oa:Choice",
                        "default": {
                            "@type": "dctypes:Image",
                            "width": 6642,
                            "height": 4990,
                            "label": "オリジナル写真",
                            "format": "image/jpeg",
                            "@id": img_obj["thumb"] # img_obj["img"]
                        },
                        "width": 6642,
                        "height": 4990,
                        "item": [
                            {
                                "label": "テキスト",
                                "@type": "dctypes:Image",
                                "@id": "https://nakamura196.github.io/genji/data/genji.png",
                                "format": "image/jpeg",
                                "width": 6642,
                                "height": 4990
                            }
                        ],

'''
