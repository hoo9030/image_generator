# generate_image.py — WebUI API 호출 기반 이미지 생성 모듈
import requests
import os
from dotenv import load_dotenv

# 공통 설정 모듈 import
from core.image_runner import get_image_config, get_default_dimensions, get_default_flags

load_dotenv()

API_URL = os.getenv("WEBUI_API", "http://127.0.0.1:7860")
OUTPUT_DIR = os.path.expanduser(os.getenv("OUTPUT_DIR", "~/stable-diffusion-webui/outputs/txt2img-images"))

def generate_image(prompt_dict: dict) -> str:
    style = prompt_dict.get("style", "default")
    prompt = prompt_dict["prompt"]

    config = get_image_config(style)
    width, height = get_default_dimensions()
    flags = get_default_flags()

    if not isinstance(prompt, str) or len(prompt.strip()) == 0:
        raise ValueError("[오류] prompt 값이 None 이거나 비어 있습니다.")

    print("=== DEBUG PAYLOAD ===")
    print("prompt:", prompt)
    print("steps:", config.get("steps"))
    print("cfg_scale:", config.get("cfg_scale"))
    print("sampler_index:", config.get("sampler_index"))

    payload = {
        "prompt": prompt,
        "steps": config["steps"],
        "cfg_scale": config["cfg_scale"],
        "sampler_index": config["sampler_index"],
        "width": width,
        "height": height,
        "batch_size": 1,
        "save_images": True,
        "enable_hr": flags["enable_hr"],
        "enable_tiled_vae": flags["enable_tiled_vae"]
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
