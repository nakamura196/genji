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




import urllib.request  # ライブラリを取り込む


target_url = 'https://textdb01.ninjal.ac.jp/LCgenji/'
r = requests.get(target_url)  # requestsを使って、webから取得

soup = BeautifulSoup(r.text, 'lxml')  # 要素を抽出

aas = soup.find_all("a")
for a in aas:
        url = a.get("href")
        if "index.html" in url and "pages" in url:
                url = target_url+url
                r2 = requests.get(url)  # requestsを使って、webから取得

                soup2 = BeautifulSoup(r2.text, 'lxml')  # 要素を抽出

                as2 = soup2.find_all("a")

                for a2 in as2:
                        url2 = a2.get("href")
                        if "UTF8" in url2:
                                url2 = target_url + url2.replace("../", "pages/")
                                print(url2)
                                filename = "data/txt/"+url2.split("/")[-1]
                                # ダウンロードを実行
                                urllib.request.urlretrieve(url2, filename)

        

        

