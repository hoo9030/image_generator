import requests
import os
import base64

# ==== 설정 ====
API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"
OUTPUT_DIR = "outputs/test_raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==== 고정 프롬프트 ====
prompt = "a simple test image"

# ==== 이미지 생성 요청 ====
response = requests.post(API_URL, json={
    "prompt": prompt,
    "steps": 10,
    "width": 16,
    "height": 16,
    "sampler_name": "Euler a",
    "enable_hr": False
})

# ==== 결과 저장 ====
if response.status_code == 200:
    image_data = response.json()['images'][0]
    image_bytes = base64.b64decode(image_data)
    output_path = os.path.join(OUTPUT_DIR, "test.png")

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print(f"[✅] 테스트 이미지 저장 완료: {output_path}")
else:
    print("[❌] 생성 실패:", response.text)
