import requests
import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import json
import ssl
import glob
ssl._create_default_https_context = ssl._create_unverified_context

files = glob.glob("data/*.json")

map = {}

for file in sorted(files):
    with open(file, 'r') as f:
        data = json.load(f)
        for key in data:
            value = data[key]

            map[key] = value

fw2 = open("data3/taisei.json", 'w')
json.dump(map, fw2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))