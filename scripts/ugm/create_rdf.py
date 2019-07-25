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

g = Graph()


def forMani(manifest, label):

    print(manifest)

    res = urllib.request.urlopen(manifest)

    # json_loads() でPythonオブジェクトに変換
    mani_data = json.loads(res.read().decode('utf-8'))

    g.add((URIRef(manifest), URIRef(
        "http://purl.org/dc/terms/subject"), URIRef("http://ja.dbpedia.org/resource/"+label)))
    g.add((URIRef("http://ja.dbpedia.org/resource/"+label), URIRef(
        "http://www.w3.org/2000/01/rdf-schema#label"), Literal(label)))

    canvases = mani_data["sequences"][0]["canvases"]

    for canvas in canvases:
        g.add((URIRef(canvas["@id"]), URIRef(
            "http://purl.org/dc/terms/isPartOf"), URIRef(manifest)))

    if "structures" in mani_data:
        for st in mani_data["structures"]:

            st_label = st["label"]

            taisei_p_uri = "http://example.org/taisei/page/"+st_label

            g.add((URIRef(st["canvases"][0]), URIRef(
                "http://purl.org/dc/terms/subject"), URIRef(taisei_p_uri)))
            g.add((URIRef(taisei_p_uri), URIRef(
                "http://www.w3.org/2000/01/rdf-schema#label"), Literal(int(st_label))))


def forCol(col_uri):
    res = urllib.request.urlopen(col_uri)

    # json_loads() でPythonオブジェクトに変換
    col_data = json.loads(res.read().decode('utf-8'))

    for manifest in col_data["manifests"]:
        forMani(manifest["@id"], manifest["label"])


universe = "https://nakamura196.github.io/genji/ugm/genji.json"

res = urllib.request.urlopen(universe)
# json_loads() でPythonオブジェクトに変換
uni_data = json.loads(res.read().decode('utf-8'))

for col in uni_data["collections"]:
    col_uri = col["@id"]

    forCol(col_uri)

g.serialize(format='pretty-xml', destination="data/test.rdf")
