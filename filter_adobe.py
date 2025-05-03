from PIL import Image
import os
import numpy as np

# 초정밀 품질 필터 (단순 예시: 해상도 + 블러 체크)
def is_image_passed(filepath):
    try:
        img = Image.open(filepath)
        width, height = img.size

        # A1: 해상도 최소 2048px
        if width < 2048 or height < 2048:
            print("[❌] 해상도 부족")
            return False

        # A4: 블러 검사 (에지 평균 계산)
        gray = img.convert('L')
        arr = np.array(gray, dtype=np.float32)
        laplacian = np.abs(np.diff(arr, axis=0)).mean() + np.abs(np.diff(arr, axis=1)).mean()
        if laplacian < 1.5:
            print("[❌] 이미지가 흐릿함")
            return False

        return True

    except Exception as e:
        print(f"[❌] 필터링 오류: {e}")
        return False
