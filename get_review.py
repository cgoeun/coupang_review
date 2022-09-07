from review import Review
import pickle
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import subprocess
import time
import pandas as pd


# 데이터 저장 (dataToCsv)
f = open('reviews.csv', 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)
title = 'rating date seller content help'.split()
writer.writerow(title)
# 다 했으면 끝에 f.close() 해줄 것.

# 쿠팡이 webdriver를 막는 것을 근거로, 기본 크롬 브라우저를 디버거 모드로 작동시켜 사용한다.
subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome('C:/Users/admin/Desktop/chromedriver.exe', options=options)

# 크롬 브라우저 내부 대기 (암묵적 대기)
driver.implicitly_wait(5)

# 복잡한 과정을 단순화하기 위해, 아래 코드로 링크를 먼저 수집하여 저장했다.
#########################################################################
# 너무 데이터 양이 방대하기 때문에,
# 자료 수집을 일단 카테고리 중 [가전/디지털]에 한정해서 크롤링해보겠습니다.
# endPage = 17 # 쿠팡 가전/디지털 랭킹 순 endPage는 17입니다.
# links = []
# for pageNum in range(1, endPage+1):
#     url = f"https://www.coupang.com/np/categories/178255?page={pageNum}"
#     driver.get(url)
#     time.sleep(2)
#     path = 'ul#productList a'
#     elems = driver.find_elements(By.CSS_SELECTOR, path)
#     for e in elems :
#         links.append(e.get_attribute('href'))

# links = list(set(links))
# with open('links.pkl', 'wb') as f:
#     pickle.dump(links, f)
#########################################################################


# 저장한 링크를 불러와서 해당 페이지에 접속하겠다.
# with open('links.pkl', 'rb') as f:
#     links = pickle.load(f)
# for test
links = ['https://www.coupang.com/vp/products/1557469098?vendorItemId=70653905177&sourceType=SDP_ALSO_VIEWED&searchId=a9a31a07e85e407ab87efe4f0fb120b9&rmdId=a9a31a07e85e407ab87efe4f0fb120b9&eventLabel=recommendation_widget_pc_sdp_001&platform=web&rmdABTestInfo=22922:A&rmdValue=p5428535616:vt-1.0.0:p1557469098&isAddedCart=',
         'https://www.coupang.com/vp/products/6645530847?itemId=15073113804&vendorItemId=82295358845&sourceType=CATEGORY&categoryId=178155&isAddedCart=']
print(len(links))

reviews = []
remove_links = 0
for url in links:
    print('get url')
    driver.get(url)
    time.sleep(3)
    path2 = '#btfTab > ul.tab-titles > li:nth-child(2)'
    driver.find_element(By.CSS_SELECTOR, path2).click()  # 상품평 보기 클릭
    print('clicked reviews')
    time.sleep(1)

    go = True
    cnt = 0
    i = 2
    t = 0
    while go:
        print('start review crawling')
        if t == 999 : go = False
        path3 = f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[{i}]'
        if i == 13: 
            i = 2
            t +=1
            path3 = f'//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[{i}]'
        driver.find_element(By.XPATH, path3).click()
        time.sleep(1)
        print('start review crawling 2')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.select(".sdp-review__article__list")
        print('get review 5, page', i-1)
        # 데이터, 즉 한 페이지 당 리뷰의 개수는 5개다.
        i += 1
        for inx, one in enumerate(data):
            if len(one) > 8:
                rv = Review()   
                print(f'data 있음 {inx}')
                rv.rating = int(one.select_one('.sdp-review__article__list__info__product-info__star-orange')['data-rating'])
                rv.date = one.select_one('.sdp-review__article__list__info__product-info__reg-date').get_text()
                rv.seller = one.select_one('.sdp-review__article__list__info__product-info__seller_name').get_text().strip()[5:]
                try: rv.content = one.select('.sdp-review__article__list__headline')[0].text.strip() + ' '
                except: pass
                try: rv.content += one.select_one('.sdp-review__article__list__review').get_text().strip().replace('\n', ' ')
                except: pass
                try: rv.help = int(one.select_one('.js_reviewArticleHelpfulCount').get_text())
                except: pass
                print(rv)
                if len(rv.content)>0 :writer.writerow(rv)
                cnt = 0
            else:
                cnt += 1
                print(f'data 없음 {cnt}')
                if cnt == 2:
                    i = 2
                    go = False
                    remove_links+=1
                    cnt = 0
        print('리뷰 end')
    print('도착~~')
f.close()
del links[:remove_links]
with open('links.pkl', 'wb') as f2:
        pickle.dump(links, f2)