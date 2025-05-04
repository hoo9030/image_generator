# prompt_generator.py — 비즈니스 프롬프트 생성기

def generate_prompt(category: str) -> str:
    if category != "business":
        raise ValueError("현재는 business 카테고리만 지원됩니다.")

    prompt = (
        "a diverse group of office workers having a meeting in a modern workspace, "
        "natural light, soft shadows, realistic skin, no distortion, commercial stock photo quality, "
        "depth of field, DSLR look, professional attire, accurate anatomy, subtle facial expressions, "
        "clean background, office furniture, collaborative posture"
    )
    return prompt
