from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import subprocess
import shutil

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
# 출처: https: // private.tistory.com/124 [오토봇팩토리:티스토리]

# 너무 데이터 양이 방대하기 때문에,
# 자료 수집을 일단 카테고리 중 [가전/디지털]에 한정해서 크롤링해보겠습니다.
subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')
options = Options()
# options = webdriver.ChromeOptions()

options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option("useAutomationExtension", False)
# options.add_experimental_option(
#     "prefs", {"prfile.managed_default_content_setting.images": 2})
driver = webdriver.Chrome(
    'C:/Users/admin/Desktop/chromedriver.exe', options=options)

# # 크롤링 방지 설정을 undefined로 변경
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#                        "source": """ Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) """})

# 크롬 브라우저 내부 대기 (암묵적 대기)
driver.implicitly_wait(5)

endPage = 17
for pageNum in range(1, 2):  # 쿠팡 가전/디지털 랭킹 순 endPage는 17입니다.
    url = f"https://www.coupang.com/np/categories/178255?page={pageNum}"
    driver.get(url)  # 1페이지에 진입
    time.sleep(2)
    path =  'ul#productList a dl'
    elems = driver.find_elements(By.CSS_SELECTOR, path)
    print(len(elems))
    for i in range(len(elems)) :
        elems[i].click()
        time.sleep(2)
        path2 = '#btfTab > ul.tab-titles > li:nth-child(2)'
        driver.find_element(By.CSS_SELECTOR, path2).click()
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        print('도착~~')
        
        driver.back()
        time.sleep(1)
        elems = driver.find_elements(By.CSS_SELECTOR, path)
        
        last_height = driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            # 끝까지 스크롤 다운
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # 1초 대기
            time.sleep(1)

            # 스크롤 다운 후 스크롤 높이 다시 가져옴
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        # path3 = 'section > article'
        # cs = driver.find_elements(By.CSS_SELECTOR, path3)
        # for idx, c in enumerate(cs):
        #     if idx == 5: break
            
                
        
        # WebDriverWait(driver, 3).until(
        #     EC.presence_of_element_located((By.XPATH, xpath))).click()
        
        # for j in range(2, 12):
        #     btn_xpath = f'/html/body/div[2]/section/div[2]/div[10]/ul[2]/li[2]/div/div[6]/section[4]/div[3]/button[{j}]'
        #     driver.find_element(By.CSS_SELECTOR, "div.sdp-review__article__page.js_reviewArticlePagingContainer > button:nth-child(2)").click()
        #     time.sleep(2)
        #     soup = BeautifulSoup(driver.page_source, 'html.parser')
        #     print(soup)
            
    
    # elems = driver.find_elements(By.CSS_SELECTOR, "a.baby-product-link")
    # for elem in elems:
    #     href = elem.get_attribute('href')
    #     script = f"window.open('{href}');"
    #     driver.execute_script(script)
    #     time.sleep(1)
    #     driver.switch_to.window(driver.window_handles[-1])
    #     print('hello')
        # driver.get(href)
        # time.sleep(3)

        # result = driver.find_elements(By.XPATH, '//*[@id="btfTab"]/ul[2]/li[2]/div/div[6]/section[4]/article')

        # for item in result:
        #     print(item)

        # driver.close()
        # driver.switch_to.window(driver.window_handles[0])


# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
# NUMBER_OF_REVIEWERS = 10
# NUMBER_OF_HISTORIES = 10


# def generate_review_list_url(product_id):
#     return f'https://www.coupang.com/vp/product/reviews?productId={product_id}&page=1&size={NUMBER_OF_REVIEWERS}&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=2&ratingSummary=true'


# def generate_history_url(reviewer_id):
#     return f'https://www.coupang.com/vp/product/reviews/profile/{reviewer_id}/reviews?page=0&size={NUMBER_OF_HISTORIES}'


# def get_reviewers(product_url):
#     product_id = urlparse(product_url).path.split('/')[-1]
#     product_html = requests.get(
#         generate_review_list_url(product_id), headers=HEADERS).text
#     soup = BeautifulSoup(product_html, 'html.parser')
#     reviewer_id_list = [elem['data-member-id']
#                         for elem in soup.find_all() if 'data-member-id' in elem.attrs]
#     return set(reviewer_id_list)


# def get_review_history(reviewer_id):
#     history_html = requests.get(generate_history_url(
#         reviewer_id), headers=HEADERS).text
#     soup = BeautifulSoup(history_html, 'html.parser')
#     history_list = [elem.text for elem in soup.find_all(
#         'div', 'sdp-review__profile__article__list__reviews__product__name')]
#     return history_list

# def main():
#     srcText = input('검색어 키워드를 입력해주세요.')
#     pass

# if __name__ == '__main__':
#     main()
#     product_url = input('상품 url을 입력해주세요')
#     reviewers = get_reviewers(product_url)
#     history_list = [get_review_history(reviewer) for reviewer in reviewers]
#     similarity = compare_histories(history_list)
#     print('유사도', similarity)
