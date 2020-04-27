import pandas as pd
import requests
import json

df = pd.read_excel('data.xlsx', index_col=None)

manifest_obj = {}
manifests = []

canvas_image_map = {}

for i in range(0, len(df.index)):
    print(df.iloc[i, 0])

    manifest = df.loc[i, "manifest"]

    if pd.isnull(manifest):
        continue

    if manifest not in manifest_obj:

        manifests.append(manifest)

        manifest_data = requests.get(manifest).json()

        manifest_obj[manifest] = {
            "within": {
                "@id": manifest,
                "@type": "sc:Manifest",
                "label": manifest_data["label"]
            },
            "members" : []
        }

        canvases = manifest_data["sequences"][0]["canvases"]

        for canvas in canvases:
            canvas_image_map[canvas["@id"]] = canvas["images"][0]["resource"]["service"]["@id"] + "/0,0,"+str(int(canvas["width"] / 2))+","+str(canvas["height"])+"/600,/0/default.jpg"

    members = manifest_obj[manifest]["members"]

    ndl_id = str(int(df.loc[i, "ndl_id"]))

    canvas_id = str(df.loc[i, "ndl_front_canvas"])

    members.append({
        "@id": canvas_id,
        "@type": "sc:Canvas",
        "label": df.loc[i, "label"],
        "metadata": [
            {
              "label": "vol",
              "value": df.loc[i, "vol"]
            },
            {
              "label": "aozora",
              "value": df.loc[i, "aozora"]
            },
            {
              "label": "tei",
              "value": df.loc[i, "tei"]
            },
            {
              "label": "ndl",
              "value": "https://dl.ndl.go.jp/info:ndljp/pid/" + ndl_id + "/" + str(int(df.loc[i, "ndl_front"])),
            },
            {
              "label": "ndl_front",
              "value": int(df.loc[i, "ndl_front"])
            },
            {
              "label": "ndl_start",
              "value": int(df.loc[i, "ndl_start"])
            },
            {
              "label": "koui_front",
              "value": int(df.loc[i, "koui_front"])
            },
            {
              "label": "koui_start",
              "value": int(df.loc[i, "koui_start"])
            },
            {
              "label": "koui_count",
              "value": int(df.loc[i, "koui_count"])
            },
            {
              "label": "jk",
              "value": "https://gateway2.itc.u-tokyo.ac.jp:11039/lib/display/?lid="+ str(df.loc[i, "jk_front"]),
            },
            {
              "label": "jk_front",
              "value": str(df.loc[i, "jk_front"])
            },
            {
              "label": "jk_start",
              "value": str(df.loc[i, "jk_start"])
            }
        ],
        "thumbnail" : canvas_image_map[df.loc[i, "ndl_front_canvas"]]
    })

selections = []
for manifest in manifests:
    selections.append(manifest_obj[manifest])

curation = {
  "@context": [
      "http://iiif.io/api/presentation/2/context.json",
      "http://codh.rois.ac.jp/iiif/curation/1/context.json"
  ],
  "@id": "https://genji.dl.itc.u-tokyo.ac.jp/data/info.json",
  "@type": "cr:Curation",
  "label": "Character List",
  "selections": selections
}

fw = open("data.json", 'w')
json.dump(curation, fw, ensure_ascii=False, indent=4, separators=(',', ': '))

