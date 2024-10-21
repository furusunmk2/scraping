# app.py
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
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
    class_tag_list = []
    
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
                    class_tag = ""
                    # corseName の要素が存在するか確認
                    corse_name_tag = tmp.find(class_='courseName')
                    corse_name = corse_name_tag.find('p').text.strip() if corse_name_tag and corse_name_tag.find('p') else "不明"

                    # 学歴のチェック
                    if re.search(r'専門', corse_name):
                        if not re.search(r"[34３４三四]", corse_name):  # 3, 4 などの条件
                            class_tag += " s2"
                        elif re.search(r"[3３三]", corse_name):
                            class_tag += " s3"
                        elif re.search(r"[4４四]", corse_name):
                            class_tag += " s4"
                    if re.search(r'高専|高度', corse_name):
                        class_tag += " s5"        
                    if re.search(r'短', corse_name):
                        class_tag += " td"
                    if re.search(r'大|学士', corse_name):
                        if not re.search(r'短|院|専門', corse_name):
                            if re.search(r'[6６六]', corse_name):
                                class_tag += " 6d"
                            else:
                                class_tag += " 4d"
                    if re.search(r'修士', corse_name):
                        class_tag += " sh"   
                    if re.search(r'博士', corse_name):
                        class_tag += " ha"
                    elif re.search(r'院', corse_name):
                        class_tag += " sh ha"   
                    if re.search(r'文系', corse_name):
                        class_tag += " bu"
                    elif re.search(r'理系', corse_name):
                        class_tag += " ri"
                    if class_tag == "":
                         class_tag += " all"  # 修正: "all" をクォーテーションで囲む

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
                    class_tag_list.append(class_tag)
                except Exception as e:
                    print(f"データの処理中にエラーが発生しました2: {e}")
                
    else:
        for i,tmp in enumerate(soup.find_all(class_="courseRow")):
            try:
                class_tag = ""
                # corseName の要素が存在するか確認
                corse_name_tag = tmp.find(class_='courseName')
                corse_name = corse_name_tag.find('p').text.strip() if corse_name_tag and corse_name_tag.find('p') else "不明"

                # 学歴のチェック
                if re.search(r'専門', corse_name):
                    if not re.search(r"[34３４三四]", corse_name):  # 3, 4 などの条件
                        class_tag += " s2"
                    elif re.search(r"[3３三]", corse_name):
                        class_tag += " s3"
                    elif re.search(r"[4４四]", corse_name):
                        class_tag += " s4"
                if re.search(r'高専|高度', corse_name):
                    class_tag += " s5"        
                if re.search(r'短', corse_name):
                    class_tag += " td"
                if re.search(r'大|学士', corse_name):
                    if not re.search(r'短|院|専門', corse_name):
                        if re.search(r'[6６六]', corse_name):
                            class_tag += " 6d"
                        else:
                            class_tag += " 4d"
                if re.search(r'修士', corse_name):
                    class_tag += " sh"   
                if re.search(r'博士', corse_name):
                    class_tag += " ha"
                elif re.search(r'院', corse_name):
                    class_tag += " sh ha"   
                if re.search(r'文系', corse_name):
                    class_tag += " bu"
                elif re.search(r'理系', corse_name):
                    class_tag += " ri"
                if class_tag == "":
                    class_tag += " all"  # 修正: "all" をクォーテーションで囲む

# s2,s3,s4,s5,td,4d,6d,sh,ha,bu,ri


                # corseData の要素が存在するか確認
                corse_data_tags = tmp.find_all(class_='courseData')
                s = corse_data_tags[0].find('p').text.strip() if len(corse_data_tags) > 0 and corse_data_tags[0].find('p') else "不明"
                d = corse_data_tags[1].find('p').text.strip() if len(corse_data_tags) > 1 and corse_data_tags[1].find('p') else "不明"
                f = corse_data_tags[2].find('p').text.strip() if len(corse_data_tags) > 2 and corse_data_tags[2].find('p') else "諸手当なし"

                graduate.append(corse_name)
                salary.append(s)
                basic.append(d)
                allowance.append(f)
                class_tag_list.append(class_tag)
            except Exception as e:
                print(f"データの処理中にエラーが発生しました1: {e}")

    # 企業のURLも一緒に返す
    return {
        "company": company,
        "company_url": url,  # URLを追加
        "graduate": graduate,
        "salary": salary,
        "basic": basic,
        "allowance": allowance,
        "class_tag_list" : class_tag_list
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
