import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from product import Product

txt = input("search :")
pageNum = 1
url = f"https://www.coupang.com/np/search?component=&q={txt}&page={pageNum}"
dr = webdriver.Chrome("/Users/admin/Desktop/chromeDriver")
dr.get(url)
myData = dr.page_source
with open("coupang.html", "w", encoding="utf-8") as f:
    f.write(myData)
dr.quit()
soup = BeautifulSoup(myData, "html.parser")
researchData = soup.select(".search-product-wrap")

l = []
for idx, item in enumerate(researchData):
    product = Product()
    product.name = researchData[idx].select(".name")[0].get_text()
    product.price = int(researchData[idx].select(".price-value")[0].get_text().replace(",", ""))
    if researchData[idx].select(".rating"):
        product.rating = float(researchData[idx].select(".rating")[0].get_text())
        product.review = int(researchData[idx].select(".rating-total-count")[0].get_text()[1:-1])
    else:
        product.rating = "평점 없음"
        product.review = "리뷰 없음"
    l.append(product)
for idx in range(len(l)):
    print(l[idx])

# for idx in range(len(l)):
#     print(l[idx])
# txt = input("search :")
# pageNum = 1
# for i in range(10):
#     url = f"https://www.coupang.com/np/search?component=&q={txt}&page={pageNum}"
#     res = requests.get(url)
#     # res.raise_for_status()
# print(res.)
#
# with open("coupang.html", "w", encoding="utf-8") as f:
#     f.write(res.text)
#
# soup = BeautifulSoup(res.text, "html.parser")
