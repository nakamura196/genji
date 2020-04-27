import pandas as pd
import requests
import json
import os
import xml.etree.ElementTree as ET
import time

hostPrefix = "https://genji.dl.itc.u-tokyo.ac.jp"
dir2 = "/Users/nakamura/git/d_genji/genji_vue/docs/data/iiif/org"


def create_members_map(members_map, members):
  for member in members:
    member_id = member["@id"]
    canvas_id = member_id.split("#")[0]
    if canvas_id not in members_map:
      members_map[canvas_id] = []
    members_map[canvas_id].append(member)

  return members_map


def create_anno(canvas, members_map, odir, index, info):

  canvas_id = canvas["@id"]

  if canvas_id not in members_map:
    return None

  odir = odir + "/list"
  os.makedirs(odir, exist_ok=True)

  opath = odir+"/p"+str(index)+".json"

  annoListUri = opath.replace(opath.split("/data/")[0], hostPrefix)

  members = members_map[canvas_id]

  resources = []

  for i in range(len(members)):
    member = members[i]

    xywh = member["@id"].split("#xywh=")[1]

    areas = xywh.split(",")

    x = int(float(areas[0]))# + int(float(areas[2]) / 2)
    y = int(float(areas[1]))

    w = int(float(areas[2]))
    h = int(float(areas[3]))

    d2 = int(w / 10)

    member_label = member["label"]

    if "metadata" not in member:
      continue

    page = int(member["metadata"][0]["value"])

    if "新編日本古典文学全集" in member_label:
      sagaId = info["jk_front"][0:-3] + str(page).zfill(3)
      chars = "新編日本古典文学全集 p."+str(page)+" 開始位置<p><a href=\"https://gateway2.itc.u-tokyo.ac.jp:11039/lib/display/?lid=" + \
                                  str(sagaId)+"\" target=\"_blank\" rel=\"noopener noreferrer\">ジャパンナレッジ</a>でみる</p>"
      fill = "#2E89D9"
      stroke = "#2E89D9"
    else:
      ndlId = info["ndl"].split("/")[-2]
      ndlPage = info["ndl_front"] + round((page - info["koui_front"]) / 2)
      chars = "源氏物語大成 p."+str(page)+" 開始位置<p><a href=\"http://dl.ndl.go.jp/info:ndljp/pid/"+ndlId+"/"+str(
          ndlPage)+"\" target=\"_blank\" rel=\"noopener noreferrer\">国立国会図書館デジタルコレクション</a>で校異源氏物語をみる</p>"
      fill = "#F3AA00"
      stroke = "#A52A2A"

    d = "M"+str(x)+","+str(y)+"h"+str(int(w / 2))+"v0h"+str(int(w / 2))+"v"+str(int(h / 2)) + \
                "v"+str(int(h / 2))+"h-"+str(int(w / 2))+"h-" + \
                        str(int(w / 2))+"v-"+str(int(h / 2))+"z"

    svg = "<svg xmlns='http://www.w3.org/2000/svg'><path xmlns=\"http://www.w3.org/2000/svg\" d=\""+d + \
        "\" id=\"pin_" + "abc" + "\" fill-opacity=\"0.8\" fill=\"" + \
            fill+"\" stroke=\""+stroke+"\"/></svg>"

    resources.append({
      "@id": annoListUri + "#" + str(i+1),
      "@type": "oa:Annotation",
      "motivation": "sc:painting",
      "on": [
          {
              "@type": "oa:SpecificResource",
              "full": canvas_id,
              "selector": {
                  "@type": "oa:Choice",
                  "default": {
                      "@type": "oa:FragmentSelector",
                      "value": "xywh=" + xywh
                  },
                  "item": {
                      "@type": "oa:SvgSelector",
                      "value": svg
                  }
              },
              "within": {
                "@id": info["manifest"],
                "@type": "sc:Manifest"
            }
          }
      ],
      "resource": {
          "@type": "dctypes:Text",
          "chars": chars,
          "format": "text/html"
      }
  })

  annoList = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": annoListUri,
    "@type": "sc:AnnotationList",
    "resources": resources
  }

  fw = open(opath, 'w')
  json.dump(annoList, fw, ensure_ascii=False, indent=4, separators=(',', ': '))

  return annoListUri


def create_manifest(selection, info):

  within = selection["within"]

  label = within["label"]

  vol = info["vol"]

  label = selection["within"]["label"]

  odir = dir2+"/"+label + "/" + str(vol).zfill(2)
  os.makedirs(odir, exist_ok=True)

  opath = odir+"/manifest.json"

  ##########

  members = selection["members"]
  members_map = {}
  members_map = create_members_map(members_map, members)

  # 東大本の場合は、新編も（あれば）

  if "東大本" in label:
    curation_uri = "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/saga/" + \
        str(vol).zfill(2)+".json"
    try:
      saga_curation = requests.get(curation_uri).json()
      members = saga_curation["selections"][0]["members"]
      members_map = create_members_map(members_map, members)
    except Exception as e:
      print("新編 does not exist.", e)

  ##########

  manifest_uri = selection["within"]["@id"]

  time.sleep(3)
  manifest_data = requests.get(manifest_uri).json()

  canvases = manifest_data["sequences"][0]["canvases"]

  for i in range(len(canvases)):
    canvas = canvases[i]
    otherContentUri = create_anno(canvas, members_map, odir, i+1, info)
    if otherContentUri:
      canvas["otherContent"] = [
          {
              "@id": otherContentUri,
              "@type": "sc:AnnotationList"
          }
      ]
    else:
      del canvas["otherContent"]

  ##########

  manifest_uri = opath.replace(opath.split("/data/")[0], hostPrefix)

  manifest_data["@id"] = manifest_uri
  manifest_data["label"] = label

  fw = open(opath, 'w')
  json.dump(manifest_data, fw, ensure_ascii=False,
            indent=4, separators=(',', ': '))

  selection["within"]["@id"] = manifest_uri

  members = []

  for canvas_id in members_map:
    for member in members_map[canvas_id]:
      members.append(member)

  selection["members"] = members

  return selection


def create_ndl(info):

  members = []

  vol = info["vol"]

  vol_str = str(vol).zfill(2)

  tei = "https://kouigenjimonogatari.github.io/tei/"+vol_str+".xml"

  response = requests.get(tei)
  if response.status_code < 400:

    xmlData = requests.get(tei).text

    root = ET.fromstring(xmlData)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")

    prefix = ".//{http://www.tei-c.org/ns/1.0}"

    surfaces = root.findall(prefix+"surface")

    for surface in surfaces:
      graphic = surface.find(prefix+"graphic")
      canvas_id = graphic.get("n")

      zones = surface.findall(prefix+"zone")

      for zone in zones:

        x = int(zone.get("ulx"))
        y = int(zone.get("uly"))

        w = int(zone.get("lrx")) - x
        h = int(zone.get("lry")) - y

        xywh = str(x) + "," + str(y) + "," + str(w) + "," + str(h)

        member_id = canvas_id+"#xywh="+xywh

        zone_id = zone.get("{http://www.w3.org/XML/1998/namespace}id")
        line_id = "https://w3id.org/kouigenjimonogatari/data/" + \
            zone_id.split("_")[1]+"-01.json"

        members.append({
          "@id": member_id,
          "@type": "sc:Canvas",
          "label": line_id,
          "line_id": line_id
        })

  selection = {
    "@id": "https://genji.dl.itc.u-tokyo.ac.jp/data/vol/"+vol_str+"/image_map.json#ndl",
    "@type": "sc:Range",
    "label": "Manual curation by IIIF Curation Viewer",
    "members": members,
    "within": {
      "@id": info["manifest"],
      "@type": "sc:Manifest",
      "label": "校異源氏物語"
    }
  }

  return selection



# print(requests.get(url).json())

# time.sleep(10)

# print(df)

# print("----------------")

def create_curations(info):
    vol = info["vol"]
    
    url = "https://us-central1-genji-5ca47.cloudfunctions.net/api/curations/" + str(vol)
    
    selections = []
    
    try:
        time.sleep(2)
        df = requests.get(url).json()["selections"]
    except Exception as e:
        print("digital genji error", url, e)
        # continue
        return []

    orderedSelections = {}
    notOrderedSelections = []

    orderedLabels = ["東大本", "九大本（古活字版）", "九大本（無跋無刊記版）"]
    
    for selection in df:
      if "members" not in selection:
        continue
      members = selection["members"]

      # すべてのアノテーション付与が完了しているもののみ
      if len(members) != info["koui_count"]:
        continue

      label = selection["within"]["label"]

      if label in orderedLabels:
          orderedSelections[label] = selection

      else:
          notOrderedSelections.append(selection)

    for label in orderedLabels:
      if label in orderedSelections:
          selection = orderedSelections[label]
          # manifestの生成
          selectionResult = create_manifest(selection, info)
          if len(selectionResult) > 0:
              selections.append(selectionResult)

    for selection in notOrderedSelections:
      # manifestの生成
      selectionResult = create_manifest(selection, info)
      if len(selectionResult) > 0:
          selections.append(selectionResult)

    return selections

def create_image_map(info, vol, dir):
  selections = []

  selections.append(create_ndl(info))

  curations = create_curations(info)

  for selection in curations:
    selections.append(selection)

  vol_str = str(vol).zfill(2)

  curation = {
    "@context": [
      "http://iiif.io/api/presentation/2/context.json",
      "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": "https://genji.dl.itc.u-tokyo.ac.jp/data/vol/"+vol_str+"/image_map.json",
    "@type": "cr:Curation",
    "label": "Curating list",
    "selections": selections
  }

  odir = dir+"/vol/"+vol_str
  os.makedirs(odir, exist_ok=True)

  fw = open(odir+"/image_map.json", 'w')
  json.dump(curation, fw, ensure_ascii=False, indent=4, separators=(',', ': '))

def create_config(info, vol, dir):
  
  vol_str = str(vol).zfill(2)

  config = {
    "return_url": "https://genji.dl.itc.u-tokyo.ac.jp/",
    "return_label": "デジタル源氏物語",
    "url_main": "https://w3id.org/kouigenjimonogatari/tei/"+vol_str+".xml" if vol < 22 else "",
    "url_sub": info["tei"],
    "url_map": "",
    "image_map": "https://genji.dl.itc.u-tokyo.ac.jp/data/vol/"+vol_str+"/image_map.json",
    "label_main": "校異源氏物語テキスト・"+info["label"],
    "label_sub": "青空文庫・与謝野晶子訳",
    "query_main": "seg[*|corresp]",
    "query_sub": "s[*|id]",
    "direction": "vertical"
  }

  odir = dir+"/vol/"+vol_str

  os.makedirs(odir, exist_ok=True)

  fw = open(odir+"/config.json", 'w')
  json.dump(config, fw, ensure_ascii=False, indent=4, separators=(',', ': '))

info = requests.get("https://raw.githubusercontent.com/nakamura196/genji_vue/master/docs/data/info.json").json()

info_map = {}

for selection in info["selections"]:
  members = selection["members"]

  manifest = selection["within"]["@id"]

  for member in members:
    metadata = member["metadata"]
    
    map = {}

    map["label"] = member["label"]
    map["manifest"] = manifest
    
    for obj in metadata:
      map[obj["label"]] = obj["value"]

      if obj["label"] == "vol":
        vol = obj["value"]

    info_map[vol] = map

dir = "/Users/nakamura/git/d_genji/genji_vue/docs/data"

for vol in range(1, 55):
  print("vol", vol)
  info = info_map[vol]
  create_image_map(info, vol, dir)
  create_config(info, vol, dir)
