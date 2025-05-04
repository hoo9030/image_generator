# tag_generator.py — BLIP 기반 키워드 및 메타데이터 생성
import os
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

def generate_metadata(image_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

    raw_image = Image.open(image_path).convert("RGB")
    inputs = processor(raw_image, return_tensors="pt").to(device)

    out = model.generate(**inputs, max_new_tokens=50)
    caption = processor.decode(out[0], skip_special_tokens=True)

    # 간단한 키워드 추출: caption 단어 분할 (정교화 가능)
    keywords = [word.strip('.,') for word in caption.split() if len(word) > 3][:10]

    title = caption.title()
    description = caption

    return title, description, ", ".join(keywords)
