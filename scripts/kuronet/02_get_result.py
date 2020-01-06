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

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(open("result.html"), "lxml")

tr_list = soup.find_all("tr")

rows = []
rows.append(["manifest", "canvas", "curation"])

print(len(tr_list))

for i in range(1, len(tr_list)):
    print(i)
    tds = tr_list[i].find_all("td")

    url_1 = tds[1].find("a").get("href").split("?")[1].split("&")
    manifest = url_1[0].split("=")[1]
    canvas = url_1[1].split("=")[1]

    a = tds[6].find("a")

    if a == None:
        continue
    
    curation = a.get("href").split("=")[1]

    rows.append([manifest, canvas, curation])

import csv

f = open('result.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()