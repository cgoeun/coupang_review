import csv
import requests
from bs4 import BeautifulSoup

url = f"http://finance.naver.com/sise/sise_market_sum.nhn?sosok=0"

fName = "test.csv"
title = "N 종목명 현재가 전일비 등랄률 액면가 시가총액 상장주식수 외국인비율 거래량 PER ROE".split()

f = open(fName, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

writer.writerow(title)

res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

data = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
for row in data:
    columns = row.find_all("td")
    if len(columns) <= 1: continue
    data = [column.get_text().strip() for column in columns]
    writer.writerow(data)
