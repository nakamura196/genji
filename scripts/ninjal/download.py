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

array = [
    {
        "prefix": "https://dglb01.ninjal.ac.jp/lcgenji_image/flex/kiritsubo/flex/dual/",
        "max": 58,
        "label": "kiritsubo"
    },
    {
        "prefix": "https://dglb01.ninjal.ac.jp/lcgenji_image/flex/suma/flex/dual/",
        "max": 66,
        "label": "suma"
    },
    {
        "prefix": "https://dglb01.ninjal.ac.jp/lcgenji_image/flex/kashiwagi/flex/dual/",
        "max": 66,
        "label": "kashiwagi"
    }
]

for obj in array:

    label = obj["label"]

    for k in range(obj["max"]+1):

        id = str(k+1).zfill(4)

        for i in range(0, 11):
            for j in range(0, 16):

                filename = "data/images/reprint_"+label + \
                    "_"+id+"_"+str(i)+"_"+str(j)+".jpg"

                if not os.path.exists(filename):

                    url = obj["prefix"]+"/reprint/reprint/"+id + \
                        "/dzc_output_files/12/" + \
                        str(i)+"_"+str(j)+".jpg"

                    print(url)

                    # ダウンロードを実行
                    try:
                        urllib.request.urlretrieve(url, filename)
                    except:
                        print("error")

                filename = "data/images/original_"+label+"_"+id+"_" + \
                    str(i)+"_"+str(j)+".jpg"

                if not os.path.exists(filename):

                    url = obj["prefix"]+"/original/original/"+id + \
                        "/dzc_output_files/12/" + \
                        str(i)+"_"+str(j)+".jpg"

                    print(url)

                   # ダウンロードを実行
                    try:
                        urllib.request.urlretrieve(url, filename)
                    except:
                        print("error")
