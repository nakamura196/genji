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
import urllib

manifest = "https://nakamura196.github.io/genji/ugm/ndl/manifest/3437686.json"

r = requests.get(manifest)
data = json.loads(r.content)

structures = data["structures"]

canvases = data["sequences"][0]["canvases"]

c_map = {}



for canvas in canvases:
    image_api = canvas["images"][0]["resource"]["service"]["@id"]+"/info.json"
    c_map[canvas["@id"]] = image_api

rows_i = []
rows_i.append(["dcterms:title", "dcterms:identifier"])

rows_m = []
rows_m.append(["Media Url", "Item Identifier"])

label_map = {}



for structure in structures:
    label = structure["label"]
    canvases = structure["canvases"]

    if label not in label_map:
        
        row_i = [label, label]
        rows_i.append(row_i)

        label_map[label] = label

    id = label_map[label]

    for canvas in canvases:
        
        
        row_m = [c_map[canvas], id]
        rows_m.append(row_m)

    # break


import csv

f = open('data/csv_item.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows_i)

f.close()

f = open('data/csv_media.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows_m)

f.close()



