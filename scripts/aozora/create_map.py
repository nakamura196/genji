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

prefix = ".//{http://www.tei-c.org/ns/1.0}"

tree = ET.parse("01.xml")
ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
root = tree.getroot()

lines = root.findall(prefix+"line")

modern_id = "-1"

map = {}

for line in lines:
    id = line.get("{http://www.w3.org/XML/1998/namespace}id")
    if len(line.findall(prefix+"anchor")) > 0:
        if modern_id != "-1":
            print(modern_id+"\t"+id)
            map[modern_id].append(id)
        for anchor in line.findall(prefix+"anchor"):
            id_anchor = anchor.get("corresp").split("#")[1]
            # print(id_anchor)
            modern_id = id_anchor

            map[modern_id] = []

    print(modern_id+"\t"+id)
    map[modern_id].append(id)

fw = open("map.json", 'w')
json.dump(map, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
