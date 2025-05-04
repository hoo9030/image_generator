# main.py — 어도비스톡 자동화 시스템 실행 파일

from prompts.prompt_generator import generate_prompt
from webui_interface.generate_image import generate_image
from metadata.tag_generator import generate_metadata
from uploader.selenium_upload import upload_to_adobestock
from utils.git_sync import push_changes

def main():
    # 1. 프롬프트 생성
    prompt = generate_prompt("business")
    print("[1] 프롬프트 생성 완료")

    # 2. 이미지 생성
    image_path = generate_image(prompt)
    print(f"[2] 이미지 생성 완료: {image_path}")

    # 3. 메타데이터 생성
    title, desc, keywords = generate_metadata(image_path)
    print("[3] 메타데이터 생성 완료")

    # 4. Adobe Stock 업로드
    upload_to_adobestock(image_path, title, desc, keywords)
    print("[4] Adobe Stock 업로드 완료")

    # 5. Git 자동 푸시
    push_changes()
    print("[5] GitHub 푸시 완료")

if __name__ == "__main__":
    main()
