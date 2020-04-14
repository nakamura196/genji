import requests
import glob
import csv
import json

'''
api_url = "https://diyhistory.org/public/genji/api"

loop_flg = True
page = 1

while loop_flg:
    url = api_url + "/media?page=" + str(
        page)
    print(url)

    page += 1

    r = requests.get(url)
    data = json.loads(r.content)

    if len(data) > 0:
        for i in range(len(data)):
            obj = data[i]
            id = obj["o:id"]

            fw = open("data/media/"+str(id)+".json", 'w')
            json.dump(obj, fw, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

    else:
        loop_flg = False
'''

mid_image_map = {}

files = glob.glob("data/media/*.json")
for file in files:
     with open(file) as f:
        df2 = json.load(f)
        mid_image_map[int(df2["o:id"])] = df2["o:source"]

'''

ids = ["3437686", "3437687", "3437688", "3437689", "3437690"]

for ndl_id in ids:

    manifest = "https://www.dl.ndl.go.jp/api/iiif/"+ndl_id+"/manifest.json"
    print(manifest)

    r = requests.get(manifest)
    data = json.loads(r.content)

    fw = open("data/manifests/"+ndl_id+".json", 'w')
    json.dump(data, fw, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))
'''

image_canvas_map = {}

files = glob.glob("data/manifests/*.json")
for file in files:
     with open(file) as f:
        df = json.load(f)
        canvases = df["sequences"][0]["canvases"]
        for i in range(len(canvases)):
            canvas = canvases[i]
            cid = canvas["@id"]
            image = canvas["images"][0]["resource"]["service"]["@id"] + "/info.json"
            image_canvas_map[image] = cid

# print(image_canvas_map)


with open('/Users/nakamura/git/d_utda/genji_private/src/org/taisei/data/data.json') as f:
    df = json.load(f)

data = {}

for line_id in df:
    text = df[line_id]
    page = int(line_id.split("-")[0])

    if page not in data:
        data[page] = []

    data[page].append(text)


test = {}

with open('data/toc.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    
    for row in reader:

        cid = row[3]


        # print(row)
        test[cid] = {
            "page" : int(row[4]),
            "project" : int(row[5])
        }

######

pid = -1

wiki_map = {}

import math

with open('data/scripto_media_all.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    
    for row in reader:
        mid = int(row[2])

        a = mid_image_map[mid]
        
        cid = image_canvas_map[a]

        if cid in test:
            pid = test[cid]["project"]

        if "3437687" in cid:
            page = 2 * (int(cid.split("/")[-1]) - 5) + 390
        elif "3437688" in cid:
            page = 2 * (int(cid.split("/")[-1]) - 5) + 800
        elif "3437689" in cid:
            page = 2 * (int(cid.split("/")[-1]) - 5) + 1222
        elif "3437690" in cid:
            # print(cid)
            page = 2 * (int(cid.split("/")[-1]) - 5) + 1672
        else:
            page = -1

        

        if page != -1 and pid != -1:

            # print(cid)

            wiki_id = "1/1/"+str(pid)+"/"+str(mid)

            pages = [page, page + 1]

            texts = []
            text_all = ""
            
            for p in pages:
                if p in data:
                    for text in data[p]:

                        arr = {
                            "將" : "将", 
                            "(の)" : "",
                            "戀" : "恋"
                        }

                        org_text = text

                        flg = False

                        for e in arr:

                            if e in text:
                                flg = True
                                text = text.replace(e, arr[e])

                        for i in range(0, len(text) - 1):
                            pt = text[i : i + 1]
                            nt = text[i + 1 : i + 2]
                            if pt == nt:
                                print(wiki_id)
                                print(text)
                                print([pt, nt])
                                text = text[0:i+1] + "ゝ" + text[i+2:len(text)]
                                print(text)
                                print("----")

                        if flg:
                            print(wiki_id)
                            print(org_text)
                            print(text)
                            print("----")

                        # texts.append(text)
                        text_all += text + "\n"

                    text_all += "\n"

            text_all = text_all.strip()
            
            if text_all != "":
                wiki_map[wiki_id.replace("/", ":")[2:]] = text_all
            



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

    print(page)

    text = wiki_map[page]

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

