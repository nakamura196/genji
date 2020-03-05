import requests
from bs4 import BeautifulSoup
import re

#初回のみ
target_url = "https://www.aozora.gr.jp/cards/000052/files/5017_9759.html"
#Requestsを使って、webから取得
r = requests.get(target_url)
#要素を抽出
soup = BeautifulSoup(r.content, 'lxml')

main_text = soup.find(class_="main_text")

text = main_text.text

print(text)

result = ""

lines = text.split("。")
count = 0
for i in range(len(lines)):
    line = lines[i].strip()

    if line != "":
        count += 1
        id = "YG"+"02"+str(count * 100).zfill(8)
        print(id)
        print(line+"。")
        print("---")

        result += "<s xml:id=\""+id+"\">"+line+"。</s>"

print(result)
        
    