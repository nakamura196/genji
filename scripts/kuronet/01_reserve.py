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

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ3NjM1YWI2NDZlMDdmZDE5OWY3NGIwMTZhOTU0MzkyMmEwY2ZmOWEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoi5Lit5p2R6KaaIiwicGljdHVyZSI6Imh0dHBzOi8vbGg1Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tR0tBdEFxVkdRRVEvQUFBQUFBQUFBQUkvQUFBQUFBQUFvQmcva1JUei1RS21LSG8vcGhvdG8uanBnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NvZGgtODEwNDEiLCJhdWQiOiJjb2RoLTgxMDQxIiwiYXV0aF90aW1lIjoxNTczNzEwNTMwLCJ1c2VyX2lkIjoiRmR6QVFvUzU4NGVXYUpOUmY1TndSTUR5QndXMiIsInN1YiI6IkZkekFRb1M1ODRlV2FKTlJmNU53Uk1EeUJ3VzIiLCJpYXQiOjE1NzY1OTQ5MjEsImV4cCI6MTU3NjU5ODUyMSwiZW1haWwiOiJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNTMxMTk4NTgxMjgyNzQ1Mjg0MiJdLCJlbWFpbCI6WyJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.EwJ6fQAzxFGvkGMxpXGyu8TnQg25tcsgamOa6V_3OvnplhN9oPXFTEzObryVwU5ePFVtEJgjwSDn9R5PhoCIUa3Lhl2htiJZUQvL3iZq9ypw6tTVvv9DaLq4xtUMxEGpBDEHd91ezjtlTsBwtogX_LbdK810Bh4GKGNpqXw4-K5olkWi3lNTX_yb7l8yYXhs8RcJvwMie8_nQ8UKi00VH2itpoFrAngcr8c5CWxduNfhYTQ2U1hvtJ4gpQKSagVhjObmBP9vCuzqi6KOOlSf-uI3Y4zN3v7taYBMggSahmDAHghxp3d23rpszKYTEvMY7XksAsqwmyVZSMDGQ1tQxA"

url = "https://mp.ex.nii.ac.jp/api/kuronet/index?token="+token

html = urllib.request.urlopen(url)

print(html)

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(html, "html.parser")

print(soup)

tr_list = soup.find_all("tr")

# rows = []
# rows.append(["manifest", "canvas", "curation"])

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
        time.sleep(1)
        req = urllib.request.Request(reserve)
        urllib.request.urlopen(req)