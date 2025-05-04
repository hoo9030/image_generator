# main.py — 어도비스톡 자동화 시스템 실행 파일 (배치 + 프롬프트 기반 메타데이터 통합)

from prompts.prompt_generator import generate_prompt
from webui_interface.generate_image import generate_image
from metadata.tag_generator import generate_metadata
from uploader.selenium_upload import upload_to_adobestock_auto
from utils.git_sync import push_changes
import time

def run_single(style="premium"):
    # 1. 프롬프트 생성
    prompt_data = generate_prompt("business", style=style)
    print("[1] 프롬프트 생성 완료")
    print("Prompt:", prompt_data["prompt"])

    # 2. 이미지 생성
    image_path = generate_image(prompt_data)
    print(f"[2] 이미지 생성 완료: {image_path}")

    # 3. 메타데이터 생성 (프롬프트 기반 키워드 병합)
    try:
        title, desc, ai_keywords = generate_metadata(image_path)
    except:
        title, desc, ai_keywords = "Untitled Business Scene", prompt_data["prompt"], []
    final_keywords = sorted(set(prompt_data["keywords"] + ai_keywords))[:49]  # Adobe 제한 고려
    print("[3] 메타데이터 생성 완료")

    # 4. Adobe Stock 업로드
    upload_to_adobestock_auto(image_path, title, desc, ", ".join(final_keywords))
    print("[4] Adobe Stock 업로드 완료")

    # 5. Git 자동 푸시
    push_changes()
    print("[5] GitHub 푸시 완료")

def run_batch(n=5, delay=10):
    for i in range(n):
        print(f"\n==== {i+1} / {n} ====")
        try:
            run_single()
        except Exception as e:
            print("[오류 발생]", e)
        time.sleep(delay)

if __name__ == "__main__":
    run_batch(n=3)
