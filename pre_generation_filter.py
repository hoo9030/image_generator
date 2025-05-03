# 프롬프트 사전 판단 필터 (엄격 적용)

BANNED_KEYWORDS = [
    "clown", "glitch", "signature", "watermark", "text",
    "words", "logo", "famous person", "celebrity", "politician",
    "gun", "weapon", "nude", "nsfw", "blood"
]

REQUIRED_COMPONENTS = [
    "lighting", "view", "quality"
]

def is_prompt_acceptable(prompt: str) -> bool:
    prompt_lower = prompt.lower()

    # 금지 키워드 검사
    for word in BANNED_KEYWORDS:
        if word in prompt_lower:
            print(f"[필터] 금지어 포함: {word}")
            return False

    # 최소 품질 요소 포함 검사
    if not any(w in prompt_lower for w in ["lighting", "light"]):
        print("[필터] 조명 관련 키워드 없음")
        return False

    if not any(w in prompt_lower for w in ["view", "angle", "perspective"]):
        print("[필터] 카메라 각도/구도 없음")
        return False

    if not any(w in prompt_lower for w in ["quality", "detailed", "photorealistic"]):
        print("[필터] 고품질 묘사 키워드 없음")
        return False

    return True
