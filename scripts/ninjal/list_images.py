import urllib.request  # ライブラリを取り込む
import csv
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


array = ["http://lcweb2.loc.gov/cgi-bin/ampage?collId=asian3&fileName=asian0001_20122008427768001page.db&recNum=",
         "http://lcweb2.loc.gov/cgi-bin/ampage?collId=asian3&fileName=asian0001_20122008427768012page.db&recNum=",
         "http://lcweb2.loc.gov/cgi-bin/ampage?collId=asian3&fileName=asian0001_20122008427768036page.db&recNum="]


rows = []

prefix = "http://lcweb2.loc.gov"

row = ["id", "img", "thumb"]
rows.append(row)

for target_url in array:

    flg = True

    page = 0

    id = target_url.split("asian0001_")[1].split("page.db")[0]

    while(flg):

        url_ = target_url+str(page)

        r = requests.get(url_)  # requestsを使って、webから取得

        soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

        aas = soup.find_all("a")

        link_count = 0

        for a in aas:
            url = a.get("href")
            if "displayPhoto" in url:

                link_count += 1

                url = prefix+url

                r2 = requests.get(url)  # requestsを使って、webから取得

                soup2 = BeautifulSoup(r2.text, 'lxml')  # 要素を抽出

                img_url = prefix + soup2.find_all(
                    "a")[0].get("href")
                thumb_url = prefix + soup2.find_all(
                    "img")[0].get("src")

                row = [id, img_url, thumb_url]
                rows.append(row)

                print(row)

                break

        if link_count == 0:
            flg = False
        else:
            page += 1


f = open('data/images.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()
