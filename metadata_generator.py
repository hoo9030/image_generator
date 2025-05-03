import os
import json
from datetime import datetime

# CLIP 기반 태그 추출은 생략하고 기본 키워드 예시 기반으로 구성
def generate_metadata(prompt, tag_count=20):
    # 제목 추출 (앞의 명사 부분)
    title = prompt.split(",")[0].strip().capitalize()

    # 설명 생성
    description = f"This image was created using generative AI. It features {prompt}. Ideal for commercial and creative use."

    # 태그 생성 (prompt 단어 기반 + 고정 태그)
    base_tags = prompt.lower().replace(",", "").split()
    fixed_tags = ["AI generated", "Generative AI"]
    all_tags = list(dict.fromkeys(base_tags + fixed_tags))[:tag_count]

    return {
        "title": title,
        "description": description,
        "tags": all_tags
    }

# 저장 예시
def save_metadata(image_path, metadata):
    base = os.path.splitext(os.path.basename(image_path))[0]
    json_path = os.path.join(os.path.dirname(image_path), f"{base}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"[📄] 메타데이터 저장 완료: {json_path}")
