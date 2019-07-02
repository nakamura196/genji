from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import os
import glob
from lxml import etree
import sys
from io import StringIO


def make_image(screen, bgcolor, filename):
    """
    画像の作成
    """
    
    #
    #ここに、いろいろな処理を追加する
    #
    
    return


if __name__ == '__main__':

    # 画像の背景色（RGB）
    bgcolor = (255, 255, 255)
    font_ttf = "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc"

    tree = ET.parse("genji.xml")
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    root = tree.getroot()

    prefix = ".//{http://www.tei-c.org/ns/1.0}"

    # 画像のサイズ
    width = 6642
    height = 4990
    screen = (width, height)

    zones = root.findall(prefix + "zone")

    # 保存するファイル名（ファイル形式は、拡張子から自動的に判別する）
    filename = "genji.png"

    img = Image.new('RGB', screen, bgcolor)

    #drawインスタンスを生成
    draw = ImageDraw.Draw(img)

    for j in range(len(zones)):
        zone = zones[j]
        id = zone.get("{http://www.w3.org/XML/1998/namespace}id")
        ulx = int(zone.get("ulx"))
        uly = int(zone.get("uly"))
        lrx = int(zone.get("lrx"))
        lry = int(zone.get("lry"))

        text = tree.find('.//*[@facs="#'+id+'"]').text

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

            #文字を書く
            draw.text((ulx, y), text[i], fill=(255, 0, 0))

    img.save(filename)
