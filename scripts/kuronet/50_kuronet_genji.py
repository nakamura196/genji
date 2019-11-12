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

manifest_uri = "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/c1ea8e6b-9403-4394-8619-96aad0ec6329/manifest"


r = requests.get(manifest_uri)
manifest_data = json.loads(r.content)

canvases = manifest_data["sequences"][0]["canvases"]

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjI1MDgxMWNkYzYwOWQ5MGY5ODE1MTE5MWIyYmM5YmQwY2ViOWMwMDQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoi5Lit5p2R6KaaIiwicGljdHVyZSI6Imh0dHBzOi8vbGg1Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tR0tBdEFxVkdRRVEvQUFBQUFBQUFBQUkvQUFBQUFBQUFvQmcva1JUei1RS21LSG8vcGhvdG8uanBnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NvZGgtODEwNDEiLCJhdWQiOiJjb2RoLTgxMDQxIiwiYXV0aF90aW1lIjoxNTUyNDA0ODM1LCJ1c2VyX2lkIjoiRmR6QVFvUzU4NGVXYUpOUmY1TndSTUR5QndXMiIsInN1YiI6IkZkekFRb1M1ODRlV2FKTlJmNU53Uk1EeUJ3VzIiLCJpYXQiOjE1NzM1NjQyMTEsImV4cCI6MTU3MzU2NzgxMSwiZW1haWwiOiJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNTMxMTk4NTgxMjgyNzQ1Mjg0MiJdLCJlbWFpbCI6WyJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.YhYVowh8qzNnOskUQrZzUTgkV5WgmOi0S0Gcey2FZvpa-GI2xanjIvllu-BD36uRYxhAsfbWZMv1Jg4gkFdmOd4NnhQYwWUonckJolaYbiF2lxFOKpWD3SZpRUlcKvwP-mHm6Hf0BrVPWSIx7jDJR21mSLtYto7OXZnJaNW-TcJNblga0FfzoXccFGRTQ51XzOWhMj0qOSUIBUCSSScFxuX_X1XnremGwXX15NeW6-8T43pwNyTdytQioJ_DNx4GErEopQpPJlhgBzMBFc7qRixCJ3Johr3Nf6EQUjrUtFExGkjv56Eb2nviiZX3wXyDO6UeoM-zm1J_SkMRUM3MRA"

lang = "ja"

post_url = "https://mp.ex.nii.ac.jp/api/kuronet/post"

for i in range(len(canvases)):

    print(i)


    canvas_obj = canvases[i]

    canvas = canvas_obj["@id"]
    image = canvas_obj["thumbnail"]["service"]["@id"]+"/1004,920,4968,3200/full/0/default.jpg"

    data = {
        "manifest": manifest_uri,
        "canvas": canvas,
        "lang": lang,
        "token": token,
        "image": image
    }

    time.sleep(5)

    response = requests.post(post_url, data=data)
    print(response.status_code)    # HTTPのステータスコード取得

    
    