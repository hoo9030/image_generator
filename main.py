# main.py — 통합 자동화 파이프라인 (기존 모듈 최대 활용)
from prompts.prompt_generator import generate_prompt
from webui_interface.generate_image import generate_image
from metadata.tag_generator import generate_metadata
from uploader.selenium_upload_auto import upload_to_adobestock_auto
from utils.git_sync import push_changes

def run_batch(n=1):
    for i in range(n):
        print(f"\n--- [ {i+1} / {n} ] 작업 시작 ---")

        # 1. 프롬프트 생성
        prompt_data = generate_prompt(category="business", style="premium")
        print("[1] 프롬프트 생성 완료")
        print("프롬프트:", prompt_data["prompt"])

        # 2. 이미지 생성
        try:
            image_path = generate_image(prompt_data)
            print(f"[2] 이미지 생성 완료: {image_path}")
        except Exception as e:
            print(f"[오류] 이미지 생성 실패: {e}")
            continue

        # 3. 메타데이터 생성
        try:
            metadata = generate_metadata(image_path, prompt_data)
            print("[3] 메타데이터 생성 완료")
        except Exception as e:
            print(f"[오류] 메타데이터 생성 실패: {e}")
            continue

        # 4. Adobe Stock 업로드
        try:
            upload_to_adobestock_auto(image_path, metadata["title"], metadata["description"], metadata["keywords"])
            print("[4] Adobe Stock 업로드 완료")
        except Exception as e:
            print(f"[오류] 업로드 실패: {e}")
            continue

        # 5. Git commit & push
        try:
            push_changes(image_path, metadata)
            print("[5] GitHub 푸시 완료")
        except Exception as e:
            print(f"[오류] Git 푸시 실패: {e}")
            continue

if __name__ == "__main__":
    run_batch(n=1)
