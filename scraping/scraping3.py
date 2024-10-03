import requests
from bs4 import BeautifulSoup

# scraping2: 企業IDを取得する
url_corp_list = "https://job.mynavi.jp/25/pc/corpinfo/searchCorpListByGenCond/index/?cond=FW:/IC:40,41,42/LICM:1/OC:293,294,340,350,360,370,380,390,400,410,415/HR:13/func=PCTopQuickSearch"

# 企業リストページを取得する
response_corp_list = requests.get(url_corp_list)
response_corp_list.encoding = response_corp_list.apparent_encoding

# BeautifulSoupで解析する
soup_corp_list = BeautifulSoup(response_corp_list.content, "html.parser")

# 企業IDを格納するリスト
corp_ids = []

# 企業IDを抽出
for info in soup_corp_list.find_all('a', class_="js-add-examination-list-text"):
    corp_ids.append(info['target'])

# 企業情報を取得する関数
def get_company_info(corp_id):
    url = f"https://job.mynavi.jp/25/pc/search/corp{corp_id}/employment.html"

    # 企業ページを取得する
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    # BeautifulSoupで解析する
    soup = BeautifulSoup(response.content, "html.parser")

    # データを格納するリスト
    graduate = []
    salary = []
    basic = []
    allowance = []

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
            
    for i in range(len(graduate)):
        print(graduate[i])
        print("支給額:" + salary[i])
        print("基本月額:" + basic[i])
        print("諸手当（一律）／月:" + allowance[i])

    # 結果をファイルに書き込む
    filename = f"{company}_data.txt"
    with open(filename, mode="w", encoding="utf-8") as f:
        f.write(f"会社名: {company}\n")
        for i in range(len(graduate)):
            f.write(f"{graduate[i]}, 支給額: {salary[i]}, 基本月額: {basic[i]}, 諸手当（一律）／月: {allowance[i]}\n")

    print(f"データが {filename} に保存されました。")

# すべての企業IDについて情報を取得
for corp_id in corp_ids:
    get_company_info(corp_id)
