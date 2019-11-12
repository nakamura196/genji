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

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1MDgxMWNkYzYwOWQ5MGY5ODE1MTE5MWIyYmM5YmQwY2ViOWMwMDQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoi5Lit5p2R6KaaIiwicGljdHVyZSI6Imh0dHBzOi8vbGg1Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tR0tBdEFxVkdRRVEvQUFBQUFBQUFBQUkvQUFBQUFBQUFvQmcva1JUei1RS21LSG8vcGhvdG8uanBnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NvZGgtODEwNDEiLCJhdWQiOiJjb2RoLTgxMDQxIiwiYXV0aF90aW1lIjoxNTczNTY4MTA1LCJ1c2VyX2lkIjoiRmR6QVFvUzU4NGVXYUpOUmY1TndSTUR5QndXMiIsInN1YiI6IkZkekFRb1M1ODRlV2FKTlJmNU53Uk1EeUJ3VzIiLCJpYXQiOjE1NzM1NjgxMTMsImV4cCI6MTU3MzU3MTcxMywiZW1haWwiOiJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNTMxMTk4NTgxMjgyNzQ1Mjg0MiJdLCJlbWFpbCI6WyJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.M2XLnQ8cHZoIlM1LUeck6rGqGyTaHX_lM1FBCU4Ae9nwMztf1znugKHelXk6rLp7oiCRlhoW2eBgIRWi1gMkDPChrhVxK4lGSKVgOOX2-xDCUJzFhr2YZv_FVlMkZnEfp6JJFucoUatbT4AlmXZK8insqyPxhwoVHxjj8cJJ3alJRMog2TRPIzVs_23F_9iOC6r6fi7NUjyiSJtN4bUII2FnTx3N3Nn99cdONjRlGjORNFGp2DyK_8VHgQ2CJcqP9dPYRH-R76qyquMJC0dxb30tiG32_p9AlXTYbCC7foG0HmDQFeawAwn2eWMZO8sqxcvyj60MeC_7gpwgx1ydug"

url = "https://mp.ex.nii.ac.jp/api/kuronet/index?token="+token

html = urllib.request.urlopen(url)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")

tr_list = soup.find_all("tr")

rows = []
rows.append(["manifest", "canvas", "curation"])

print(len(tr_list))

for i in range(len(tr_list)):
    print(i)
    tds = tr_list[i].find_all("td")

    a = tds[3].find("a")

    if a == None:
        continue

    reserve = a.get("href")

    a = tds[6].find("a")
    
    if a == None:
        time.sleep(20)
        req = urllib.request.Request(reserve)
        urllib.request.urlopen(req)