# prompt_generator.py — 주제별 프롬프트 동적 생성기
import random
import time
import hashlib

def generate_prompt(category: str, style: str = "default", seed: int = None) -> str:
    if seed is None:
        seed = int(hashlib.sha256(str(time.time()).encode()).hexdigest(), 16) % (10**8)
    random.seed(seed)

    if category != "business":
        raise ValueError("지원되지 않는 카테고리입니다.")

    parts = []

    # 스타일 설명
    style_intro_map = {
        "minimal": "Minimalist composition, soft tones, clean layout",
        "premium": "Premium lighting setup, editorial-grade color grading",
        "casual": "Natural pose, casual dress code, warm tone",
        "default": "High-quality stock photo style"
    }
    parts.append(style_intro_map.get(style, style_intro_map["default"]))

    # 인트로
    parts.append(random.choice([
        "A diverse group of professionals in a modern office",
        "An energetic team of coworkers",
        "A collaborative corporate team",
        "A group of colleagues working together",
        "Business professionals in a tech-driven environment"
    ]))

    # 동작
    parts.append(random.choice([
        "collaborating on a project", "engaged in strategic planning",
        "brainstorming with visual aids", "analyzing reports and charts",
        "pitching ideas to clients", "leading a group presentation"
    ]))

    # 소품 및 배치
    parts.append(random.choice([
        "with laptops, tablets, and printed documents",
        "using whiteboards, markers, and projectors",
        "around a conference table with visuals",
        "near large screens displaying data",
        "sharing input via sticky notes and diagrams"
    ]))

    # 복장
    parts.append(random.choice([
        "dressed in professional attire",
        "wearing business casual outfits",
        "in coordinated team colors",
        "with branded name tags and badges"
    ]))

    # 표정 및 제스처
    parts.append(random.choice([
        "confident and focused expressions",
        "smiling and nodding in agreement",
        "intense and thoughtful demeanor",
        "relaxed but attentive posture"
    ]))

    # 조명 조건
    parts.append(random.choice([
        "natural light from large windows",
        "soft diffused office lighting",
        "even light with warm tones",
        "bright ambient illumination"
    ]))

    # 배경 묘사
    parts.append(random.choice([
        "clean background with minimal decor",
        "modern office interior with glass walls",
        "creative workspace with plants and posters",
        "executive suite with high-end furniture"
    ]))

    # 품질 및 리얼리즘
    parts.append(random.choice([
        "realistic skin textures, no distortion, DSLR clarity",
        "photorealistic details, commercial-grade sharpness",
        "balanced exposure and natural tones",
        "depth of field, AI-free appearance"
    ]))

    # 구도 설명
    parts.append(random.choice([
        "framed with whitespace for text",
        "rule-of-thirds layout with central focus",
        "horizontal format for web banners",
        "designed with ad space consideration"
    ]))

    # 카메라 세부 묘사
    parts.append(random.choice([
        "shot with wide-angle lens",
        "captured at f/2.8 with shallow DOF",
        "DSLR-style capture with 50mm lens",
        "photographed using natural light bokeh effect"
    ]))

    # 메타데이터
    metadata = f"(prompt_id: {seed}, style: {style})"

    return ", ".join(parts) + f", compliant with Adobe Stock quality guidelines. {metadata}"
