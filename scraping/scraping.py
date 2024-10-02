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
print(soup.find("title").text)

company = soup.find("title", class_= "company")
print(company.text)
# print(response.text)

filename = "download.txt"
f = open(filename, mode = "w")
f.write(response.text)
f.close()
