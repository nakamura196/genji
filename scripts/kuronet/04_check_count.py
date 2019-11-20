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


curation_uri = "https://raw.githubusercontent.com/nakamura196/genji/master/docs/kuronet/5008825ba0abc69f9cda5399eda3aa46.json"

r = requests.get(curation_uri)
data = json.loads(r.content)

members = data["selections"][0]["members"]

hist = {}

for member in members:
    member_id = member["@id"]
    canvas_id = member_id.split("#")[0]

    if canvas_id not in hist:
        hist[canvas_id] = 0

    hist[canvas_id] += 1

for canvas_id in hist:
    print(canvas_id+"\t"+str(hist[canvas_id]))
