import re
import requests
from bs4 import BeautifulSoup

url = "https://job.mynavi.jp/25/pc/corpinfo/searchCorpListByGenCond/index/?cond=FW:/IC:40,41,42/LICM:1/OC:293,294,340,350,360,370,380,390,400,410,415/HR:13/func=PCTopQuickSearch"

# webページを取得する
response = requests.get(url)
response.encoding = response.apparent_encoding

# BeautifulSoupで解析する
soup = BeautifulSoup(response.content, "html.parser")

# データを格納するリスト
graduate = []
salary = []
basic = []
allowance = []
corp_id = []

for info in soup.find_all('a',class_="js-add-examination-list-text"):

    corp_id.append(info['target'])

print(corp_id)




# 会社名を取得
company_mod = soup.find("title").text
company = company_mod.replace("の採用データ | マイナビ2025", "")
print("会社名:", company)

# 各コースの情報を取得
for tmp in soup.find_all(class_="courseRow"):
    try:
        # 各要素を分割
        a, s, d, f = tmp.text.split()
        graduate.append(a)
        salary.append(s)
        basic.append(d)
        allowance.append(f)
    except ValueError:
        print("データを分割できませんでした:", tmp.text)
# for i in range(4):
#     print(graduate[1])
#     print("支給額:" + salary[i])
#     print("基本月額:" + basic[i])
#     print("諸手当（一律）／月:" + allowance[i])


# 結果をファイルに書き込む
filename = "download.txt"
with open(filename, mode="w", encoding="utf-8") as f:  # コンテキストマネージャを使用
    f.write(response.text)

print(f"データが {filename} に保存されました。")

