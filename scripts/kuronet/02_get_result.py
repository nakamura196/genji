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
import difflib
import time
import urllib

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1MDgxMWNkYzYwOWQ5MGY5ODE1MTE5MWIyYmM5YmQwY2ViOWMwMDQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoi5Lit5p2R6KaaIiwicGljdHVyZSI6Imh0dHBzOi8vbGg1Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tR0tBdEFxVkdRRVEvQUFBQUFBQUFBQUkvQUFBQUFBQUFvQmcva1JUei1RS21LSG8vcGhvdG8uanBnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NvZGgtODEwNDEiLCJhdWQiOiJjb2RoLTgxMDQxIiwiYXV0aF90aW1lIjoxNTUyNDA0ODM1LCJ1c2VyX2lkIjoiRmR6QVFvUzU4NGVXYUpOUmY1TndSTUR5QndXMiIsInN1YiI6IkZkekFRb1M1ODRlV2FKTlJmNU53Uk1EeUJ3VzIiLCJpYXQiOjE1NzM1NzE0MjMsImV4cCI6MTU3MzU3NTAyMywiZW1haWwiOiJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNTMxMTk4NTgxMjgyNzQ1Mjg0MiJdLCJlbWFpbCI6WyJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.Sxenf879-FaBJzS2rgW2om-5X4rBXCm27PyGw8qp3FlHTKdrLmXvY2Itw7cSwyhYSW3a8VFOevbDpqYN7dCakUd13CRYi92KG8GO-GKkGwoVfwR8-Nd364ei2LY-XYZHmo6j3INJdBtFNng6OwSgi5Zw9SHLD4KHigVvKWh5M74mUtPmYUIgNNSh-XlYY86XCXAdTPH2m-LadDoHkHfi0Vdiu0bLKBI09c0E_3Cks-BcV5APAFIwLhsxKJiRffTtlwzaqwZa1zGO-0SfgLuepFmdiNEIl7NVUDmHgknTvuGYH-gaMaObjpCwTN_NA7u02PERoWWkyYJj70LNt06IwQ"

url = "https://mp.ex.nii.ac.jp/api/kuronet/index?token="+token

html = urllib.request.urlopen(url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")

tr_list = soup.find_all("tr")

rows = []
rows.append(["manifest", "canvas", "curation"])

print(len(tr_list))

for i in range(1, len(tr_list)):
    print(i)
    tds = tr_list[i].find_all("td")

    url_1 = tds[1].find("a").get("href").split("?")[1].split("&")
    manifest = url_1[0].split("=")[1]
    canvas = url_1[1].split("=")[1]

    a = tds[6].find("a")

    if a == None:
        continue
    
    curation = a.get("href").split("=")[1]

    rows.append([manifest, canvas, curation])

import csv

f = open('result.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()