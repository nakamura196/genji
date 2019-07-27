import requests
import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import json
import ssl
import glob
import difflib
import pandas as pd

imap = {}

with open("data3/taisei.json", 'r') as f:
    data = json.load(f)

    for key in sorted(data):
        keys = key.split("-")
        page = keys[0]

        if page not in imap:
            imap[page] = ""

        imap[page] += data[key]

tmap = {}

with open("data3/saga.json", 'r') as f:
    data = json.load(f)

    for key in sorted(data):
        keys = key.split("-")
        page = keys[2]+"-"+keys[0]

        if page not in imap:
            tmap[page] = ""

        tmap[page] += data[key]

rows = []
row = ["i", "t", "sim"]
rows.append(row)


for i in imap:
    value = imap[i]
    max_index = -1
    max_sim = -1

    for t in tmap:

        tvalue = tmap[t]


        s = difflib.SequenceMatcher(None, value, tvalue).ratio()

        if s > max_sim:
            max_sim = s
            max_index = t

    row = [i, max_index, max_sim]
    print(row)
    rows.append(row)

    # break

df = pd.DataFrame(rows)
df.to_excel('data3/compare.xlsx',
            index=False, header=False)
