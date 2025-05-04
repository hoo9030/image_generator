# generate_image.py — WebUI 이미지 생성 모듈
import requests
import os

def generate_image(prompt: str) -> str:
    api_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

    payload = {
        "prompt": prompt,
        "steps": 30,
        "sampler_index": "DPM++ 2M Karras",
        "cfg_scale": 7,
        "width": 2560,
        "height": 1600,
        "batch_size": 1,
        "save_images": True
    }

    response = requests.post(api_url, json=payload)
    response.raise_for_status()
    result = response.json()

    # WebUI에서 저장된 이미지 경로 추론
    output_dir = os.path.expanduser("~/stable-diffusion-webui/outputs/txt2img-images")
    latest_file = max(
        [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".png")],
        key=os.path.getctime
    )
    return latest_file
