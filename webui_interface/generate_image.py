# generate_image.py — WebUI 이미지 생성 모듈 with 스타일 기반 설정
import requests
import os
import time

def generate_image(prompt_dict: dict) -> str:
    api_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

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

    response = requests.post(api_url, json=payload)
    response.raise_for_status()
    result = response.json()

    output_dir = os.path.expanduser("~/stable-diffusion-webui/outputs/txt2img-images")
    latest_file = max(
        [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".png")],
        key=os.path.getctime
    )
    return latest_file
