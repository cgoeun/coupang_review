import requests
from bs4 import BeautifulSoup
from mysqlConnector import *
from book import Book

url = "https://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?kind=2"

res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

myR = soup.select_one(".list_type01").select(".detail")
bookList = []
for x in myR:
    bookList.append(Book(
        x.find("a")["onclick"].split("', '")[0][-13:],
        x.find("strong").get_text(),
        x.find("a")["onclick"].split("', '")[5],
        x.find("a")["onclick"].split("', '")[3],
        x.find("div", {"class": "author"}).get_text().split("|")[2].strip(),
        x.find("div", {"class": "review"}).find("img")["alt"][-2:-1],
        x.find("div", {"class": "review"}).find("a").get_text()[1:-12],
        x.find("strong", {"class": "book_price"}).get_text().replace(",", "").strip()[:-1]))
for book in bookList:
    print(book)
