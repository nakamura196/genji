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
    ["をとめ", 21, 661],

    ["玉かつら", 22, 715],
    ["初音", 23, 759],
    ["こてふ", 24, 777],
    ["ほたる", 25, 801],
    ["とこなつ", 26, 825],
    ["かゝり火", 27, 851],
    ["野わき", 28, 859],
    ["みゆき", 29, 881],
    ["藤はかま", 30, 913],
    ["まきはしら", 31, 931],
    ["梅かえ", 32, 971],
    ["藤のうらは", 33, 993],
    ["わかな上", 34, 1021],
    ["わかな下", 35, 1121],
    ["かしは木", 36, 1223],
    ["よこ笛", 37, 1265],
    ["すゝむし", 38, 1287],
    ["夕きり", 39, 1305],
    ["みのり", 40, 1377],
    ["まほろし", 41, 1399],
    ["にほふ兵部卿", 42, 1425],
    ["こうはい", 43, 1443],
    ["たけ川", 44, 1459],
    ["はし姬", 45, 1503],
    ["しゐかもと", 46, 1543],
    ["あけまき", 47, 1583],
    ["さわらひ", 48, 1673],
    ["やとり木", 49, 1697],
    ["あつまや", 50, 1789],
    ["うき舟", 51, 1855],
    ["かけろふ", 52, 1927],
    ["てならひ", 53, 1985],
    ["夢のうきはし", 54, 2051]

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
