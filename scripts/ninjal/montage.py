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

import urllib.request  # ライブラリを取り込む

c = 10
r = 15

array = [
    {
        "prefix": "https://dglb01.ninjal.ac.jp/lcgenji_image/flex/kiritsubo/flex/dual/",
        "max": 58,
        "label": "kiritsubo"
    }
]

lines = []

for obj in array:

        label = obj["label"]

        for k in range(obj["max"]+1):

                id = str(k+1).zfill(4)

                line = "montage "

                # id = str(5).zfill(4)

                for j in range(0, r+1):
                        for i in range(0, c+1):
                        
                                # line += "data/images/"+id+"_"+str(i)+"_"+str(j)+".jpg "
                                line += "data/images/reprint_"+label + \
                                "_"+id+"_"+str(i)+"_"+str(j)+".jpg "

                line += "-tile "+str(c+1)+"x"+str(r+1)+" -geometry +0+0 "
                line += "data/reprint_"+label+"_"+id+".jpg"

                print(line)
                lines.append([line])

                line = "montage "

                for j in range(0, r+1):
                        for i in range(0, c+1):

                                # line += "data/images/"+id+"_"+str(i)+"_"+str(j)+".jpg "
                                line += "data/images/original_"+label + \
                                    "_"+id+"_"+str(i)+"_"+str(j)+".jpg "

                line += "-tile "+str(c+1)+"x"+str(r+1)+" -geometry +0+0 "
                line += "data/original_"+label+"_"+id+".jpg"

                print(line)
                lines.append([line])


f = open('batch.sh', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(lines)

f.close()
