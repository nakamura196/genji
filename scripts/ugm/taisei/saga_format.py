import requests
import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import json
import ssl
import glob
ssl._create_default_https_context = ssl._create_unverified_context

files = glob.glob("data2/*.json")

page_before = -1
book = 1

map = {}

for file in sorted(files):
    with open(file, 'r') as f:
        data = json.load(f)
        for key in data:
            value = data[key]

            key = key.replace("��", "")

            keys = key.split("-")

            page = int(key[0])
            line = int(key[1])

            if page < page_before:
                book += 1

            page_before = page

            # print(book)

            key = key+"-"+str(book)

            print(key + "\t" + value)

            map[key] = value

fw2 = open("data3/saga.json", 'w')
json.dump(map, fw2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))