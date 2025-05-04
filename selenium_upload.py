# selenium_upload.py — 어도비스톡 자동 업로드
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json
import os

def upload_to_adobestock(image_path, title, desc, keywords):
    # 크롬 드라이버 설정
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    # 로그인 정보 불러오기
    with open("uploader/credential.json", "r") as f:
        cred = json.load(f)

    driver.get("https://contributor.stock.adobe.com")
    time.sleep(3)

    # 로그인 절차
    driver.find_element(By.LINK_TEXT, "로그인").click()
    time.sleep(2)
    driver.find_element(By.ID, "EmailPage-EmailField").send_keys(cred["email"])
    driver.find_element(By.ID, "EmailPage-ContinueButton").click()
    time.sleep(2)
    driver.find_element(By.ID, "PasswordPage-PasswordField").send_keys(cred["password"])
    driver.find_element(By.ID, "PasswordPage-SignInButton").click()
    time.sleep(5)

    # 업로드 페이지 이동
    driver.get("https://contributor.stock.adobe.com/en/uploads")
    time.sleep(3)

    # 이미지 업로드
    upload_input = driver.find_element(By.XPATH, '//input[@type="file"]')
    upload_input.send_keys(os.path.abspath(image_path))
    time.sleep(10)  # 업로드 대기

    # 메타데이터 입력은 파일 업로드 이후 수동 또는 추가 구현 필요

    print("[AdobeStock] 업로드 완료 (메타데이터 입력은 생략됨)")
    driver.quit()
