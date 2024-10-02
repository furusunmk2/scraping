import requests
from bs4 import BeautifulSoup


url = "https://job.mynavi.jp/25/pc/corpinfo/displayEmployment/index?corpId=215524&recruitingCourseId=108859"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser") 

#ここでwebページを取得する。
response = requests.get(url)

#文字化け防止コード
response.encoding = response.apparent_encoding

#取得した文字列データを出力する。
company_mod = soup.find("title").text
company = company_mod.replace("の採用データ | マイナビ2025","")
print(company)

salary_mod = soup.find(class_="courseName").text
salary = salary_mod
print(salary)

for graduate in soup.find_all(class_="courseRow"):
    print(graduate.text)
    # for j in soup.find_all(class_="courseData"):
    #     print(j.text)
# print(response.text)

filename = "download.txt"
f = open(filename, mode = "w")
f.write(response.text)
f.close()




    # <tr class="courseRow">
    #     <th class="courseName">
    #             <p>大学（通信・電気電子・情報システム系）</p>
    #     </th>
    #     <td class="courseData">
    #             <p><span class="payTypeCd10">（月給）</span>215,000円</p>
    #     </td>
    #     <td class="courseData">
    #             <p>205,000円</p>
    #     </td>
    #     <td class="courseData">
    #             <p>10,000円</p>
    #     </td>
    # </tr>