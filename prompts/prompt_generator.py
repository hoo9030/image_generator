# prompt_generator.py — 주제별 프롬프트 생성기
import os

def generate_prompt(category: str) -> str:
    base_path = os.path.join(os.path.dirname(__file__), "templates")
    template_path = os.path.join(base_path, f"{category}.txt")

    if not os.path.exists(template_path):
        raise ValueError(f"지원하지 않는 카테고리입니다: {category}")

    with open(template_path, "r", encoding="utf-8") as f:
        prompt = f.read().strip()

    return prompt
