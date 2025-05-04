# generate_image.py — WebUI 이미지 생성 모듈 with 스타일 기반 설정 (dotenv 연동)
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("WEBUI_API", "http://127.0.0.1:7860")
OUTPUT_DIR = os.path.expanduser(os.getenv("OUTPUT_DIR", "~/stable-diffusion-webui/outputs/txt2img-images"))

def generate_image(prompt_dict: dict) -> str:
    style = prompt_dict.get("style", "default")
    prompt = prompt_dict["prompt"]

    style_config = {
        "default": {"steps": 30, "cfg_scale": 7.0, "sampler_index": "DPM++ 2M Karras"},
        "minimal": {"steps": 25, "cfg_scale": 6.5, "sampler_index": "DPM++ SDE Karras"},
        "premium": {"steps": 35, "cfg_scale": 8.5, "sampler_index": "DPM++ 2M SDE Karras"},
        "casual": {"steps": 28, "cfg_scale": 6.0, "sampler_index": "Euler a"},
    }
    config = style_config.get(style, style_config["default"])

    payload = {
        "prompt": prompt,
        "steps": config["steps"],
        "cfg_scale": config["cfg_scale"],
        "sampler_index": config["sampler_index"],
        "width": 2560,
        "height": 1600,
        "batch_size": 1,
        "save_images": True
    }

    response = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload)
    response.raise_for_status()
    result = response.json()

    if not os.path.exists(OUTPUT_DIR):
        raise FileNotFoundError(f"OUTPUT_DIR 경로가 존재하지 않습니다: {OUTPUT_DIR}")

    latest_file = max(
        [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")],
        key=os.path.getctime
    )
    return latest_file
