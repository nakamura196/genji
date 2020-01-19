#!/usr/bin/python3

"""
    edit.py
    MediaWiki API Demos
    Demo of `Edit` module: POST request to edit a page
    MIT license
"""

import requests

import csv
import json

S = requests.Session()

URL = "https://diyhistory.org/public/genji/wiki2/api.php"

rows = []

with open('data/scripto_media.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        id = row[3]

        id = id.replace("/", ":")[2:]

        # print(id)

        arr = []
        if row[4] != "":
            arr.append(int(row[4]))
        if row[5] != "":
            arr.append(int(row[5]))

        if len(arr) == 0:
            continue

        print(arr)

        # Step 1: GET Request to fetch login token
        PARAMS_0 = {
            "action": "query",
            "format": "json",
            "titles": id,
            "rvprop": "content",
            "prop": "revisions"
        }

        R = S.get(url=URL, params=PARAMS_0)
        pages = R.json()["query"]["pages"]
        for key in pages:
            data = pages[key]["revisions"][0]["*"].split("\n")

            k = 0
            l = 0

            for i in range(len(data)):
                text = data[i]
                if text == "":
                    k += 1
                    l = 0
                else:

                    if k >= len(arr):
                        continue

                    page = str(arr[k])
                    index = str(l+1)

                    l += 1

                    row = ["https://w3id.org/kouigenjimonogatari/data/"+page.zfill(4)+"-"+index.zfill(2)+".json", page, index, data[i]]
                    rows.append(row)

with open('data/output.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(rows)