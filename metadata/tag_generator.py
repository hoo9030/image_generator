# tag_generator.py — 이미지 기반 메타데이터 자동 생성
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

def generate_metadata(image_path, prompt_data=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

    raw_image = Image.open(image_path).convert("RGB")
    inputs = processor(raw_image, return_tensors="pt").to(device)
    out = model.generate(**inputs, max_new_tokens=50)

    caption = processor.decode(out[0], skip_special_tokens=True)

    metadata = {
        "title": caption.title(),
        "description": caption,
        "keywords": ", ".join(caption.split()[:10])
    }

    return metadata
