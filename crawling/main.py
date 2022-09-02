import requests
from bs4 import BeautifulSoup

# dr = webdriver.chrome("Users/admin/Desktop./chromedriver")

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)  # requests를 통해 url을 타고 들어간다!
res.raise_for_status()  # 문제가 생기면 진행이 안 되도록 되어 있다! 제대로 받으면 ㅇㅋ!
print(len(res.text))  # 뽑아온 코드가 몇 글자니!

# with open("webtoon.html","w",encoding="utf-8") as f :
#             f.write(re.text)

soup = BeautifulSoup(res.text, "html.parser")
myList = soup.ol.select("a")
for x in myList:
   rank = x["onclick"].split(",")
   print(f"{x.get_text()} // 랭킹 : {rank[3][1:-2]}")


myList = soup.find_all("ol")
result = myList[1].select("li")
for x in result:
    print(x["class"][0], x.find("a")["title"])
    # print(x["class"][0], x.select("a")[0]["title"])
    # print(x["class"][0], x.select("a")[0].get_text())
# myList = soup.find_all("ol")
# print(myList[1])
# print(myList[1].select("a")[0].get_text().strip().split("-")[0])

# for x in myList:
#     print(x["class"][0], x.select("a")[0].get_text())

