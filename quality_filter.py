# quality_filter.py — AdobeStock 기준 기반 품질 필터링 (OCR + 해상도 + 흐림 + NSFW + 유사도 감지)
from PIL import Image
import cv2
import numpy as np
import pytesseract
import os
from transformers import pipeline
import imagehash
import hashlib

# ✅ NSFW 감지 파이프라인 초기화 (transformers)
safety_checker = pipeline("image-classification", model="Falconsai/nsfw_image_detection")

# ✅ 유사 이미지 저장용 해시 캐시
HASH_CACHE_PATH = "approved_hashes.txt"
def load_existing_hashes():
    if os.path.exists(HASH_CACHE_PATH):
        with open(HASH_CACHE_PATH, "r") as f:
            return set(line.strip() for line in f)
    return set()

def save_hash(new_hash: str):
    with open(HASH_CACHE_PATH, "a") as f:
        f.write(new_hash + "\n")


def is_quality_acceptable(image_path: str) -> tuple[bool, str | None]:
    """
    Adobe Stock 승인 기준에 따라 이미지 품질 필터링
    - 해상도, 흐림, 텍스트, NSFW, 유사도
    """
    if not os.path.exists(image_path):
        return False, "이미지 파일이 존재하지 않음"

    try:
        img = Image.open(image_path).convert("RGB")

        # ✅ 해상도 필터 (픽셀 수 기준, 최소 4MP)
        total_pixels = img.width * img.height
        if total_pixels < 4_000_000:
            return False, f"해상도 부족: {img.width}x{img.height} = {total_pixels:,} 픽셀 ({total_pixels / 1_000_000:.2f}MP)"

        # ✅ 흐림 감지
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        laplacian_var = cv2.Laplacian(img_cv, cv2.CV_64F).var()
        if laplacian_var < 100:
            return False, f"흐림 감지됨 (Laplacian 분산: {laplacian_var:.2f})"

        # ✅ 텍스트 포함 여부 (OCR)
        ocr_text = pytesseract.image_to_string(img)
        if len(ocr_text.strip()) > 5:
            return False, f"텍스트 포함 감지됨: '{ocr_text.strip()[:30]}...'"

        # ✅ NSFW 감지 (transformers 기반)
        nsfw_result = safety_checker(img)[0]
        if nsfw_result["label"].lower() != "safe" and nsfw_result["score"] > 0.5:
            return False, f"NSFW 감지됨: {nsfw_result['label']} ({nsfw_result['score']:.2f})"

        # ✅ 유사 이미지 감지 (hash 기반)
        hash_value = str(imagehash.average_hash(img))
        existing_hashes = load_existing_hashes()
        if hash_value in existing_hashes:
            return False, "중복 이미지 감지됨 (해시 일치)"

        save_hash(hash_value)

        return True, None

    except Exception as e:
        return False, f"이미지 검사 중 오류 발생: {e}"
