import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

result = {}

def scrape_for_page(url, page):
    flg = True

    sleep(1)

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    sp = str(soup).split("<hr/>")[2].split("<br/>")

    if len(sp) > 1:

        line = sp[0].strip()

        prefix = line.split(" ")[0].strip()

        print("page\t" + str(page) + "\t"+prefix)

        text = line[len(prefix)+1:].strip()
        
        if prefix not in result:
            result[prefix] = text

            obj = {
                prefix : text
            }

            fw2 = open("data/"+str(page).zfill(6)+"_"+prefix+".json", 'w')
            json.dump(obj, fw2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))


    else:
        flg = False

    return flg


if __name__ == '__main__':

    

    output_path = "data/list.json"

    base_url = "http://www.genji.co.jp/taisei-genji-sub.php?file=all.txt&code="

    loop_flg = True
    page = 28560

    while loop_flg:
        url = base_url + str(page)

        loop_flg = scrape_for_page(url, page)

        page += 1

    fw2 = open(output_path, 'w')
    json.dump(result, fw2, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
