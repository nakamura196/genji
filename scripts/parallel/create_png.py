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

prefix = ".//{http://www.tei-c.org/ns/1.0}"
odir = "../docs/data"
prefix_uri = "https://nakamura196.github.io/genji/data/"


def get_manifest_data(manifest_uri):
    r = requests.get(manifest_uri)
    manifest_data = json.loads(r.content)
    return manifest_data


def create_anno(surface, manifest_data, md5, index, anno_arr):

    canvases = manifest_data["sequences"][0]["canvases"]
    canvas = canvases[index]

    anno_filename = "p"+str(index+1).zfill(4)+".json"

    dir = odir+"/"+md5 + "/list"
    os.makedirs(dir, exist_ok="true")

    output_path = dir + "/" + anno_filename

    annolist_id = prefix_uri + output_path.split("/data/")[1]

    annolist = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": annolist_id,
        "@type": "sc:AnnotationList",
        "resources": []
    }

    for i in range(len(anno_arr)):
        obj = anno_arr[i]

        x = obj["ulx"]
        y = obj["uly"]
        w = obj["lrx"] - x
        h = obj["lry"] - y

        text = obj["text"]

        if text != None:

            anno = {
                "@id": annolist["@id"]+"#"+str(i),
                "@type": "oa:Annotation",
                "motivation": "sc:painting",
                "resource": {
                    "@type": "cnt:ContentAsText",
                    "chars": text,
                    "format": "text/plain"
                },
                "on": canvas["@id"] + "#xywh=" + str(x) + ","+str(y)+","+str(w)+","+str(h)
            }
            annolist["resources"].append(anno)

    fw = open(output_path, 'w')
    json.dump(annolist, fw, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))

    return annolist["@id"]


def create_img(surface, manifest_data, md5, index, anno_arr, width, height):

    # 画像のサイズ
    screen = (width, height)

    dir = odir+"/"+md5 + "/layer"
    os.makedirs(dir, exist_ok="true")

    # 保存するファイル名（ファイル形式は、拡張子から自動的に判別する）
    filename = "p"+str(index+1).zfill(4)+".png"

    img = Image.new('RGB', screen, bgcolor)

    # drawインスタンスを生成
    draw = ImageDraw.Draw(img)

    for obj in anno_arr:

        ulx = obj["ulx"]
        uly = obj["uly"]
        lrx = obj["lrx"]
        lry = obj["lry"]
        text = obj["text"]

        if text != None:

            x = lrx - ulx
            y = lry - uly

            l = len(text)

            dy = y / l

            d = dy
            if d > x:
                d = x

            draw.font = ImageFont.truetype(font_ttf, int(d))

            for i in range(l):
                y = uly + i * d

                # 文字を書く
                draw.text((ulx, y), text[i], fill=(255, 0, 0))

    output_path = dir + "/" + filename

    img.save(output_path)

    return prefix_uri + output_path.split("/data/")[1]


def handle_surface(surface, manifest_data, md5):

    index = -1

    canvas_id = surface.find(prefix + "graphic").get("n")

    width = -1
    height = -1

    canvases = manifest_data["sequences"][0]["canvases"]
    for i in range(len(canvases)):
        canvas = canvases[i]
        if canvas_id == canvas["@id"]:
            index = i

            width = canvas["width"]
            height = canvas["height"]

            break

    canvas = canvases[index]

    zones = surface.findall(prefix + "zone")

    anno_arr = []

    for j in range(len(zones)):
        zone = zones[j]
        id = zone.get("{http://www.w3.org/XML/1998/namespace}id")
        ulx = int(zone.get("ulx"))
        uly = int(zone.get("uly"))
        lrx = int(zone.get("lrx"))
        lry = int(zone.get("lry"))

        text = None

        text_arr = tree.findall('.//*[@facs="#'+id+'"]')

        if len(text_arr) > 0:

            text = text_arr[0].text

        obj = {
            "ulx": ulx,
            "uly": uly,
            "lrx": lrx,
            "lry": lry,
            "text": text
        }

        anno_arr.append(obj)

    anno_uri = create_anno(surface, manifest_data, md5, index, anno_arr)
    canvas["otherContent"] = [
        {
            "@id": anno_uri,
            "@type": "sc:AnnotationList"
        }
    ]

    img_url = create_img(surface, manifest_data, md5,
                         index, anno_arr, width, height)

    resource = canvas["images"][0]["resource"]
    resource["label"] = "Original"

    canvas["images"][0]["resource"] = {
        "@type": "oa:Choice",
        "default": resource,
        "item": [
            {
                "label": "Other",
                "@type": "dctypes:Image",
                "@id": img_url,
                "format": "image/jpeg",
                "width": width,
                "height": height
            }
        ]
    }


if __name__ == '__main__':

    # 画像の背景色（RGB）
    bgcolor = (255, 255, 255)
    font_ttf = "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"

    tree = ET.parse("genji.xml")
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    manifest_uri = root.find(prefix + "surfaceGrp").get("facs")
    md5 = hashlib.md5(manifest_uri.encode()).hexdigest()

    os.makedirs(odir+"/"+md5, exist_ok="true")

    manifest_data = get_manifest_data(manifest_uri)

    surface_arr = root.findall(prefix+"surface")

    for surface in surface_arr:
        handle_surface(surface, manifest_data, md5)

    dir = odir+"/"+md5

    tei_url = prefix_uri + "genji.xml"

    url = "https://iiif.dl.itc.u-tokyo.ac.jp/api/iiif-search/generator.php?tei=" + tei_url
    search_uri = get_manifest_data(url)[0]

    manifest_data["service"] = {
        "@context": "http://iiif.io/api/search/0/context.json",
        "@id": search_uri,
        "profile": "http://iiif.io/api/search/0/search",
        "label": "Search within this manifest"
    }

    fw = open(dir+"/manifest.json", 'w')
    json.dump(manifest_data, fw, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
