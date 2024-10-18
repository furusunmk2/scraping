from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 企業IDリストを取得する関数
def get_corp_ids():
    url_corp_list = "https://job.mynavi.jp/25/pc/corpinfo/searchCorpListByGenCond/index/?cond=FW:/IC:40,41,42/LICM:1/OC:293,294,340,350,360,370,380,390,400,410,415/HR:13/func=PCTopQuickSearch"
    response_corp_list = requests.get(url_corp_list)
    response_corp_list.encoding = response_corp_list.apparent_encoding
    soup_corp_list = BeautifulSoup(response_corp_list.content, "html.parser")

    corp_ids = []
    for info in soup_corp_list.find_all('a', class_="js-add-examination-list-text"):
        corp_ids.append(info['target'])

    return corp_ids

# 企業情報を取得する関数
def get_company_info(corp_id):
    # 企業ページのURLを生成
    url = f"https://job.mynavi.jp/25/pc/search/corp{corp_id}/employment.html"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, "html.parser")

    graduate = []
    salary = []
    basic = []
    allowance = []

    company_mod = soup.find("title").text
    company = company_mod.replace("の採用データ | マイナビ2025", "")
    company = company.replace("の募集コース一覧 | マイナビ2025", "")
    
    # 各コースの情報を取得
    if not soup.find_all(class_="courseRow"):
        url_corp_list2 = f"https://job.mynavi.jp/25/pc/search/corp{corp_id}/employment.html"
        response_corp_list2 = requests.get(url_corp_list2)
        response_corp_list2.encoding = response_corp_list2.apparent_encoding
        soup_corp_list = BeautifulSoup(response_corp_list2.content, "html.parser")
       
        # viewDataListのリンクを取得
        corp_ids2 = []
        for info in soup_corp_list.find_all("a", id=lambda x: x and "viewDataList" in x):
            href = info["href"]
            full_url = f"https://job.mynavi.jp{href}"  # hrefが部分パスの可能性があるため、フルURLを構成
            corp_ids2.append(full_url)
        
        # corp_ids2リストのURLからデータを取得
        for url_corp_list3 in corp_ids2:
            response = requests.get(url_corp_list3)
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.content, "html.parser")

            for tmp in soup.find_all(class_="courseRow"):
                try:
                    # corseName の要素が存在するか確認
                    corse_name_tag = tmp.find(class_='courseName')
                    corse_name = corse_name_tag.find('p').text.strip() if corse_name_tag and corse_name_tag.find('p') else "不明"

                    # corseData の要素が存在するか確認
                    corse_data_tags = tmp.find_all(class_='courseData')
                    s = corse_data_tags[0].find('p').text.strip() if len(corse_data_tags) > 0 and corse_data_tags[0].find('p') else "不明"
                    d = corse_data_tags[1].find('p').text.strip() if len(corse_data_tags) > 1 and corse_data_tags[1].find('p') else "不明"
                    f = corse_data_tags[2].find('p').text.strip() if len(corse_data_tags) > 2 and corse_data_tags[2].find('p') else "諸手当なし"

                    graduate.append(corse_name)
                    salary.append(s)
                    basic.append(d)
                    allowance.append(f)
                except Exception as e:
                    print(f"データの処理中にエラーが発生しました2: {e}")
                
    else:
        for tmp in soup.find_all(class_="courseRow"):
            try:
                # corseName の要素が存在するか確認
                corse_name_tag = tmp.find(class_='courseName')
                corse_name = corse_name_tag.find('p').text.strip() if corse_name_tag and corse_name_tag.find('p') else "不明"

                # corseData の要素が存在するか確認
                corse_data_tags = tmp.find_all(class_='courseData')
                s = corse_data_tags[0].find('p').text.strip() if len(corse_data_tags) > 0 and corse_data_tags[0].find('p') else "不明"
                d = corse_data_tags[1].find('p').text.strip() if len(corse_data_tags) > 1 and corse_data_tags[1].find('p') else "不明"
                f = corse_data_tags[2].find('p').text.strip() if len(corse_data_tags) > 2 and corse_data_tags[2].find('p') else "諸手当なし"

                graduate.append(corse_name)
                salary.append(s)
                basic.append(d)
                allowance.append(f)
            except Exception as e:
                print(f"データの処理中にエラーが発生しました1: {e}")

    # 企業のURLも一緒に返す
    return {
        "company": company,
        "company_url": url,  # URLを追加
        "graduate": graduate,
        "salary": salary,
        "basic": basic,
        "allowance": allowance
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    corp_ids = get_corp_ids()
    results = []
    for corp_id in corp_ids:
        results.append(get_company_info(corp_id))
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
