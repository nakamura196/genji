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

tree = ET.parse("01_koui_yosano.xml")
ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
root = tree.getroot()


lines = root.findall(prefix+"seg")

sub_previous_id = "-1"

map = {}

for j in range(len(lines)):
    line = lines[j]

    id = line.get("corresp")

    sub_ids = []

    if len(line.findall(prefix+"anchor")) > 0:
        for anchor in line.findall(prefix+"anchor"):
            if "#" not in anchor.get("corresp"):
                continue
            id_anchor = anchor.get("corresp").split("#")[1]
            sub_ids.append(id_anchor)

    print(sub_ids)

    # print(sub_ids)

    soup = BeautifulSoup(ET.tostring(line, encoding="utf-8", method="xml"), "xml") # 第2引数でパーサを指定
    line_html = soup.find("seg")

    line_text = line_html.decode_contents(formatter="html").strip()
        
    line_parts = re.split('<.+?/>', line_text)
    # print(line_parts)

    index = 0

    print(line_parts)

    for i in range(len(line_parts)):
        line_part = line_parts[i].strip()

        if line_part == "":
            continue

        print(line_part)

        start = index
        end = start + len(line_part)

        main_id = id+"#"+str(start)+":"+str(end)

        sub_id = ""

        print(sub_ids)
        print("---")

        print(i)

        if i == 0:
            sub_id = sub_previous_id
        else:
            sub_id = sub_ids[i-1]

        if sub_id not in map:
            map[sub_id] = []
        map[sub_id].append(main_id)

        index = end

    if len(sub_ids) > 0:
        sub_previous_id = sub_ids[-1]

fw = open("map_words4koui.json", 'w')
json.dump(map, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
