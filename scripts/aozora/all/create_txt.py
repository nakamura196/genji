import requests
from bs4 import BeautifulSoup
import re

start = 5016
end = 5071

index = 1

for i in range(start, end + 1):
    url = "https://www.aozora.gr.jp/cards/000052/card"+str(i)+".html"

    r = requests.get(url)
    #要素を抽出
    soup = BeautifulSoup(r.content, 'lxml')

    a_arr = soup.find_all("a")

    for a in a_arr:
        href = a.get("href")

        if href != None and "files/"+str(i)+"_" in href and ".html" in href:
            target_url = "https://www.aozora.gr.jp/cards/000052/files/" + href.split("/files/")[1]
            print(target_url)

            #Requestsを使って、webから取得
            r = requests.get(target_url)
            #要素を抽出
            soup = BeautifulSoup(r.content, 'lxml')

            main_text = soup.find(class_="main_text")

            text = main_text.text

            # print(text)

            result = ""

            lines = text.split("。")
            count = 0
            for i in range(len(lines)):
                line = lines[i].strip()

                if line != "":
                    count += 1
                    id = "YG"+str(index).zfill(2)+str(count * 100).zfill(8)

                    '''
                    print(id)
                    print(line+"。")
                    print("---")
                    '''

                    result += "<s xml:id=\""+id+"\">"+line+"。</s>"

            prefix = '''<?xml version="1.0" encoding="utf-8"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?><?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title>Title</title>
            </titleStmt>
            <publicationStmt>
                <p>Publication Information</p>
            </publicationStmt>
            <sourceDesc>
                <p>Information about the source</p>
            </sourceDesc>
        </fileDesc>
    </teiHeader>
    <text>
        <body>
            <p>
            
            '''

            # print(result)

            suffix = '''
            
           </p>
        </body>
    </text>
</TEI>
            
            '''

            opath = "data/"+str(index).zfill(2)+".xml"

            '''
            with open(opath, mode='w') as f:
                f.write(prefix+result+suffix)
            '''

            index += 1

            break
        
    