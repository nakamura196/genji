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

with open('/Users/nakamura/git/d_utda/genji_private/src/org/taisei/data/data.json') as f:
    df = json.load(f)

data = {}

for line_id in df:
    text = df[line_id]
    page = int(line_id.split("-")[0])

    if page not in data:
        data[page] = []

    data[page].append(text)

wiki_map = {}

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
        
        if len(arr) > 0:
            wiki_map[id] = arr

S = requests.Session()

URL = "https://diyhistory.org/public/genji/wiki2/api.php"

# Step 1: GET Request to fetch login token
PARAMS_0 = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_0)
DATA = R.json()

LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Step 2: POST Request to log in. Use of main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
PARAMS_1 = {
    "action": "login",
    "lgname": "nakamura",
    "lgpassword": "AwW58GJLww",
    "lgtoken": LOGIN_TOKEN,
    "format": "json"
}

R = S.post(URL, data=PARAMS_1)

# Step 3: GET request to fetch CSRF token
PARAMS_2 = {
    "action": "query",
    "meta": "tokens",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS_2)
DATA = R.json()

CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

for page in wiki_map:
    arr = wiki_map[page]
    text = ""
    for k in arr:

        if k in data:
            texts = data[k]

            for t in texts:
                text += t + "\n"

            text += "\n"


    # Step 4: POST request to edit a page
    PARAMS_3 = {
        "action": "edit",
        "title": page,
        "token": CSRF_TOKEN,
        "format": "json",
        "text": text
    }

    R = S.post(URL, data=PARAMS_3)
    DATA = R.json()

    print(DATA)