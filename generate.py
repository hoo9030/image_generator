import requests
import os
import json
from datetime import datetime

# ==== 설정 ====
API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"
OUTPUT_DIR = "outputs/raw"
PROMPT_GENERATOR = "prompt_generator.py"
PRE_FILTER = "pre_generation_filter.py"

# ==== 출력 디렉토리 생성 ====
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==== 프롬프트 생성 ====
from prompt_generator import generate_prompt
from pre_generation_filter import is_prompt_acceptable

prompt = generate_prompt()

if not is_prompt_acceptable(prompt):
    print("[❌] 프롬프트가 사전 기준을 통과하지 못했습니다. 이미지 생성을 중단합니다.")
    exit()

print(f"[🟢] 사용 프롬프트: {prompt}")

# ==== 이미지 생성 요청 ====
response = requests.post(API_URL, json={
    "prompt": prompt,
    "negative_prompt": "lowres, bad anatomy, blurry, text, error, cropped, jpeg artifacts, signature, watermark",
    "steps": 30,
    "cfg_scale": 8,
    "width": 1024,
    "height": 1536,
    "sampler_name": "DPM++ 2M Karras",
    "enable_hr": True,
    "hr_scale": 2,
    "hr_upscaler": "Latent",
    "hr_second_pass_steps": 20,
    "denoising_strength": 0.4
})

# ==== 결과 저장 ====
if response.status_code == 200:
    result = response.json()
    image_data = result['images'][0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"img_{timestamp}.png")

    with open(output_path, "wb") as f:
        f.write(requests.get(f"data:image/png;base64,{image_data}".split(",")[1]).content)

    print(f"[✅] 이미지 저장 완료: {output_path}")
else:
    print("[❌] 이미지 생성 실패:", response.text)
