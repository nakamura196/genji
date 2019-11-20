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
import xmljson
from lxml.etree import parse
import re

prefix = ".//{http://www.tei-c.org/ns/1.0}"

tree = ET.parse("../aozora/01.xml")
ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
root = tree.getroot()

surfaceGrp = root.find(prefix+"surfaceGrp")
surfaces = surfaceGrp.findall(prefix+"surface")

manifest = surfaceGrp.get("facs")

members = []

for j in range(len(surfaces)):
    surface = surfaces[j]

    canvas = surface.find(prefix+"graphic").get("n")
    zones = surface.findall(prefix+"zone")

    for k in range(len(zones)):
        zone = zones[k]
        x = int(zone.get("ulx"))
        y = int(zone.get("uly"))
        w = int(zone.get("lrx")) - x
        h = int(zone.get("lry")) - y
        member_id = canvas+"#xywh="+str(x)+","+str(y)+","+str(w)+","+str(h)

        line_id = zone.find(prefix+"line").get("{http://www.w3.org/XML/1998/namespace}id")

        members.append(
          {
            "@id": member_id,
            "@type": "sc:Canvas",
            "label": line_id
          }
        )

curation_uri = "ex:test"

curation_data = {
    "@context": [
      "http://iiif.io/api/presentation/2/context.json",
      "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@type": "cr:Curation",
    "@id": curation_uri,
    "label": "Curating list",
    "selections": [
      {
        "@id": curation_uri+"/range1",
        "@type": "sc:Range",
        "label": "Manual curation by IIIF Curation Viewer",
        "members": members,
        "within": {
          "@id": manifest,
          "@type": "sc:Manifest",
          "label": "源氏物語 第1冊（国文学研究資料館）"
        }
      }
    ]
  }

fw = open("curation.json", 'w')
json.dump(curation_data, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))

