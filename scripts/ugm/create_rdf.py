import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json
import urllib.request
import os
import requests

g = Graph()

target = ""

def forMani(manifest):

    print(manifest)

    res = urllib.request.urlopen(manifest)

    # json_loads() でPythonオブジェクトに変換
    mani_data = json.loads(res.read().decode('utf-8'))

    canvases = mani_data["sequences"][0]["canvases"]

    for canvas in canvases:

        g.add((URIRef(canvas["@id"]), URIRef(
            "http://purl.org/dc/terms/isPartOf"), URIRef(manifest)))
        g.add((URIRef(canvas["@id"]), URIRef(
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://iiif.io/api/presentation/2#Canvas")))

        if "otherContent" in canvas:


            anno_uri = canvas["otherContent"][0]["@id"]
            print(anno_uri)

            anno_data = requests.get(anno_uri).json()

            g.add((URIRef(anno_uri), URIRef(
                "http://purl.org/dc/terms/isPartOf"), URIRef(canvas["@id"])))
            g.add((URIRef(anno_uri), URIRef(
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://iiif.io/api/presentation/2#AnnotationList")))

            resources = anno_data["resources"]

            for resource in resources:

                chars = resource["resource"]["chars"].split(" ")

                ref_label = chars[0]

                st_label = chars[1].split(".")[1]

                page_uri = ""
                class_uri = ""

                if ref_label == "校異源氏物語":
                    page_uri = "http://example.org/taisei/page/"+st_label
                    class_uri = "http://example.org/class/TaiseiPageID"
                else:
                    page_uri = "https://japanknowledge.com/lib/display/?lid=80110V00200" + \
                        str(st_label).zfill(3)
                    class_uri = "http://example.org/class/SagaPageID"

                g.add((URIRef(anno_uri), URIRef(
                    "http://purl.org/dc/terms/subject"), URIRef(page_uri)))
                g.add((URIRef(page_uri), URIRef(
                    "http://www.w3.org/2000/01/rdf-schema#label"), Literal(int(st_label))))
                
                g.add((URIRef(page_uri), URIRef(
                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef(
                    class_uri)))

        

def forCol(col_uri):

    res = urllib.request.urlopen(col_uri)


    # json_loads() でPythonオブジェクトに変換
    col_data = json.loads(res.read().decode('utf-8'))

    g.add((URIRef(col_uri), URIRef(
        "http://www.w3.org/2000/01/rdf-schema#label"), Literal(col_data["label"])))
    g.add((URIRef(col_uri), URIRef(
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://iiif.io/api/presentation/2#Collection")))

    for manifest in col_data["manifests"]:

        manifest_uri = manifest["@id"]
        label = manifest["label"]

        forMani(manifest_uri)

        g.add((URIRef(manifest_uri), URIRef(
            "http://purl.org/dc/terms/isPartOf"), URIRef(col_uri)))
        g.add((URIRef(manifest_uri), URIRef(
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://iiif.io/api/presentation/2#Manifest")))
        g.add((URIRef(manifest_uri), URIRef(
            "http://purl.org/dc/terms/subject"), URIRef("http://ja.dbpedia.org/resource/"+label)))

        g.add((URIRef("http://ja.dbpedia.org/resource/"+label), URIRef(
            "http://www.w3.org/2000/01/rdf-schema#label"), Literal(label)))

universe = "https://nakamura196.github.io/genji/ugm/genji.json"

res = urllib.request.urlopen(universe)
# json_loads() でPythonオブジェクトに変換
uni_data = json.loads(res.read().decode('utf-8'))

for col in uni_data["collections"]:
    col_uri = col["@id"]

    if target != "" and target not in col_uri:
        continue

    forCol(col_uri)

g.serialize(format='pretty-xml', destination="data/data.rdf")
