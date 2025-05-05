# main_postprocess.py — WebUI에서 수동 생성한 이미지 후처리 자동화
import os
import glob
from prompts.prompt_generator import generate_prompt
from metadata.tag_generator import generate_metadata
from uploader.selenium_upload_auto import upload_to_adobestock_auto
from utils.git_sync import push_changes
from quality_filter import is_quality_acceptable

# ✅ 1. 최신 이미지 자동 탐색
def get_latest_image(folder="outputs/txt2img-images"):
    folders = sorted([f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))])
    if not folders:
        raise FileNotFoundError("[오류] 생성된 이미지 폴더가 없습니다.")

    latest_dir = os.path.join(folder, folders[-1])
    image_list = glob.glob(os.path.join(latest_dir, "*.png"))
    if not image_list:
        raise FileNotFoundError("[오류] 해당 폴더에 PNG 이미지가 없습니다: " + latest_dir)

    return max(image_list, key=os.path.getctime)


def postprocess_webui_image():
    print("\n=== WebUI 수동 이미지 후처리 자동 실행 ===")

    image_path = get_latest_image()
    print(f"[1] 이미지 파일 찾음: {image_path}")

    # ✅ 품질 필터링 검사
    ok, reason = is_quality_acceptable(image_path)
    if not ok:
        print(f"[필터링] 업로드 중단됨 → 사유: {reason}")
        return

    # 프롬프트 정보 수동 지정 필요
    prompt_data = {
        "prompt": "Business team discussion scene in modern startup office",
        "style": "premium"
    }

    metadata = generate_metadata(image_path, prompt_data)
    print("[2] 메타데이터 생성 완료")

    upload_to_adobestock_auto(image_path, metadata["title"], metadata["description"], metadata["keywords"])
    print("[3] Adobe Stock 업로드 완료")

    push_changes(image_path, metadata)
    print("[4] GitHub 푸시 완료")


if __name__ == "__main__":
    postprocess_webui_image()
