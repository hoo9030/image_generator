from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import os

UPLOAD_DIR = "outputs/passed"

def upload_adobe(image_path, metadata):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    # 1. Adobe Stock 로그인 페이지 접속
    driver.get("https://contributor.stock.adobe.com")
    input("[🟡] 로그인 후 Enter 키를 눌러주세요...")

    # 2. 업로드 탭 이동
    driver.get("https://contributor.stock.adobe.com/en/uploads")
    time.sleep(2)

    # 3. 파일 업로드
    upload_input = driver.find_element(By.XPATH, '//input[@type="file"]')
    upload_input.send_keys(os.path.abspath(image_path))
    print(f"[⏫] 업로드 중: {image_path}")
    time.sleep(5)

    # 4. 메타데이터 입력 대기 및 자동 입력 (간단 예시)
    title = metadata["title"]
    description = metadata["description"]
    tags = metadata["tags"]

    input("[🟡] 수동 입력 또는 자동화 추가 구현 가능. Enter로 종료.")
    driver.quit()

# 실행 예시
def auto_upload_all():
    for file in os.listdir(UPLOAD_DIR):
        if file.endswith(".png"):
            base = os.path.splitext(file)[0]
            img_path = os.path.join(UPLOAD_DIR, file)
            json_path = os.path.join(UPLOAD_DIR, base + ".json")
            if os.path.exists(json_path):
                with open(json_path, encoding="utf-8") as f:
                    metadata = json.load(f)
                upload_adobe(img_path, metadata)

if __name__ == "__main__":
    auto_upload_all()
