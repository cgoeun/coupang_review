import requests
from bs4 import BeautifulSoup

url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=영화&oquery=dudghk&tqi=hV0BadprvhGssK5irsVsssssshR-026770"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "html.parser")

data = soup.select(".data_area")
for idx, x in enumerate(data):
    img_url = x.find("img")["src"]
    img_res = requests.get(img_url)
    img_res.raise_for_status()

    with open (f"mo_thumb_{idx}.jpg","wb") as f:
        f.write(img_res.content)

