import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("/Users/admin/Desktop/chromeDriver")
driver.get("https://www.naver.com")

time.sleep(1)
    # Get element with tag name 'div'
element = driver.find_element(By.CLASS_NAME, "link_login")
element.click()

myId = driver.find_element(By.CLASS_NAME, "id")
myId.send_keys("everynetflix")
myPass = driver.find_element(By.ID, "pw")
myPass.send_keys("gpwjd2554")
btn = driver.find_element(By.ID, "log.login")
btn.click()