import os
from generate import prompt, OUTPUT_DIR
from filter_adobe import is_image_passed
from metadata_generator import generate_metadata, save_metadata
from upload_adobe import upload_adobe

# 마지막으로 생성된 이미지 파일 가져오기
latest_image = sorted(
    [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")],
    key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)),
    reverse=True
)[0]

image_path = os.path.join(OUTPUT_DIR, latest_image)

# 1. 품질 필터 검사
if not is_image_passed(image_path):
    print("[❌] 이미지 품질 기준 미달. 업로드 중단.")
    exit()

# 2. 메타데이터 생성 및 저장
metadata = generate_metadata(prompt)
save_metadata(image_path, metadata)

# 3. 업로드 실행
upload_adobe(image_path, metadata)
