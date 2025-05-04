# selenium_upload_auto.py — 어도비스톡 자동 업로드 + 메타데이터 자동 입력 (dotenv 연동)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv

load_dotenv()

ADOBE_EMAIL = os.getenv("ADOBE_EMAIL")
ADOBE_PASSWORD = os.getenv("ADOBE_PASSWORD")

def upload_to_adobestock_auto(image_path, title, desc, keywords):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    driver.get("https://contributor.stock.adobe.com")
    time.sleep(3)

    driver.find_element(By.LINK_TEXT, "로그인").click()
    time.sleep(2)
    driver.find_element(By.ID, "EmailPage-EmailField").send_keys(ADOBE_EMAIL)
    driver.find_element(By.ID, "EmailPage-ContinueButton").click()
    time.sleep(2)
    driver.find_element(By.ID, "PasswordPage-PasswordField").send_keys(ADOBE_PASSWORD)
    driver.find_element(By.ID, "PasswordPage-SignInButton").click()
    time.sleep(5)

    driver.get("https://contributor.stock.adobe.com/en/uploads")
    time.sleep(3)

    upload_input = driver.find_element(By.XPATH, '//input[@type="file"]')
    upload_input.send_keys(os.path.abspath(image_path))
    time.sleep(15)  # 업로드 대기

    # 이미지 선택 후 자동 메타데이터 입력
    try:
        driver.find_element(By.CSS_SELECTOR, "div.asset-title input").clear()
        driver.find_element(By.CSS_SELECTOR, "div.asset-title input").send_keys(title)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "div.asset-description textarea").clear()
        driver.find_element(By.CSS_SELECTOR, "div.asset-description textarea").send_keys(desc)
        time.sleep(1)
        keyword_input = driver.find_element(By.CSS_SELECTOR, "div.asset-keywords input")
        keyword_input.clear()
        keyword_input.send_keys(keywords)
        keyword_input.send_keys(Keys.ENTER)
        time.sleep(1)
    except Exception as e:
        print("[메타데이터 입력 오류]", e)

    print("[AdobeStock] 업로드 및 메타데이터 입력 완료")
    driver.quit()
