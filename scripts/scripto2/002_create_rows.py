import bs4
import requests
from urllib.parse import urljoin
import uuid
import json
import pandas as pd
import openpyxl

confs = [
    ["すま", 12, 391],
    ["あかし", 13, 437],
    ["みをつくし", 14, 479],
    ["よもきふ", 15, 515],
    ["せきや", 16, 543],
    ["ゑあはせ", 17, 553],
    ["松かせ", 18, 575],
    ["うす雲", 19, 599],
    ["あさかほ", 20, 635],
    ["をとめ", 21, 661]
]

rows = []

for conf in confs:
    title = conf[0]
    vol = conf[1]
    start_page = conf[2] + 4

    print(vol)

    file = "data/"+title+".json"

    

    with open(file, 'r') as f:
        data = json.load(f)

        members = data["selections"][0]["members"]

        manifest = data["selections"][0]["within"]["@id"]

        for i in range(len(members)):
            member = members[i]

            text = member["metadata"][0]["value"].split("\n")

            canvas_uri = member["@id"].split("#")[0]

            canvas_id = canvas_uri.split("/")[-1]
            # page = start_page + (canvas_id - start_canvas)

            line_num = 1

            for line in text:

                if line.strip() != "":

                    line = line.strip()

                    

                    row = [
                        "https://w3id.org/kouigenjimonogatari/data/" + str(start_page).zfill(4) + "-" + str(line_num).zfill(2) + ".json",
                        start_page,
                        line_num,
                        line,
                        "http://creativecommons.org/publicdomain/zero/1.0/",
                        title,
                        vol,
                        "源氏物語",
                        "https://jpsearch.go.jp/term/type/文章要素",
                        "",
                        "",
                        canvas_id,
                        canvas_uri,
                        manifest,
                        "http://da.dl.itc.u-tokyo.ac.jp/mirador/?params=[{%22manifest%22:%22"+manifest+"%22,%22canvas%22:%22"+canvas_uri+"%22}]"
                    ]

                    rows.append(row)

                    line_num += 1
                else:
                    # 空行の場合
                    line_num = 1
                    start_page += 1

            
            start_page += 1


df = pd.DataFrame(rows)

df.to_excel('data2/result.xlsx',index=False, header=False)
