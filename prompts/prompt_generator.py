# prompt_generator.py — 주제별 프롬프트 동적 생성기 + 확장 + 고급 기능
import random
import time
import hashlib
import os
import json

# 프롬프트 구성요소 리스트로 분리
INTRO = [
    "A diverse group of professionals in a modern office",
    "An energetic team of coworkers",
    "A collaborative corporate team",
    "A group of colleagues working together",
    "Business professionals in a tech-driven environment"
]

ACTION = [
    "collaborating on a project", "engaged in strategic planning",
    "brainstorming with visual aids", "analyzing reports and charts",
    "pitching ideas to clients", "leading a group presentation"
]

OBJECTS = [
    "with laptops, tablets, and printed documents",
    "using whiteboards, markers, and projectors",
    "around a conference table with visuals",
    "near large screens displaying data",
    "sharing input via sticky notes and diagrams"
]

CLOTHING = [
    "dressed in professional attire",
    "wearing business casual outfits",
    "in coordinated team colors",
    "with branded name tags and badges"
]

EXPRESSION = [
    "confident and focused expressions",
    "smiling and nodding in agreement",
    "intense and thoughtful demeanor",
    "relaxed but attentive posture"
]

LIGHTING = [
    "natural light from large windows",
    "soft diffused office lighting",
    "even light with warm tones",
    "bright ambient illumination"
]

BACKGROUND = [
    "clean background with minimal decor",
    "modern office interior with glass walls",
    "creative workspace with plants and posters",
    "executive suite with high-end furniture"
]

QUALITY = [
    "realistic skin textures, no distortion, DSLR clarity",
    "photorealistic details, commercial-grade sharpness",
    "balanced exposure and natural tones",
    "depth of field, AI-free appearance"
]

COMPOSITION = [
    "framed with whitespace for text",
    "rule-of-thirds layout with central focus",
    "horizontal format for web banners",
    "designed with ad space consideration"
]

CAMERA = [
    "shot with wide-angle lens",
    "captured at f/2.8 with shallow DOF",
    "DSLR-style capture with 50mm lens",
    "photographed using natural light bokeh effect"
]

LOCATION = [
    "in a high-rise building in New York",
    "in a Seoul startup hub",
    "inside a Silicon Valley tech office",
    "within a Scandinavian-style coworking space"
]

STYLE_INTRO_MAP = {
    "minimal": "Minimalist composition, soft tones, clean layout",
    "premium": "Premium lighting setup, editorial-grade color grading",
    "casual": "Natural pose, casual dress code, warm tone",
    "default": "High-quality stock photo style"
}

LOG_PATH = "generated_prompts.txt"

# 중복 확인용
def is_duplicate(prompt: str) -> bool:
    if not os.path.exists(LOG_PATH):
        return False
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return prompt.strip() in f.read()

def save_prompt_log(prompt: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(prompt.strip() + "\n")

def generate_prompt(category: str, style: str = "default", seed: int = None, dedupe: bool = True) -> dict:
    max_attempts = 10
    attempt = 0
    while attempt < max_attempts:
        attempt += 1

        if seed is None:
            seed = int(hashlib.sha256(str(time.time()).encode()).hexdigest(), 16) % (10**8)
        random.seed(seed)

        if category != "business":
            raise ValueError("지원되지 않는 카테고리입니다.")

        parts = [
            STYLE_INTRO_MAP.get(style, STYLE_INTRO_MAP["default"]),
            random.choice(INTRO),
            random.choice(ACTION),
            random.choice(OBJECTS),
            random.choice(CLOTHING),
            random.choice(EXPRESSION),
            random.choice(LIGHTING),
            random.choice(BACKGROUND),
            random.choice(LOCATION),
            random.choice(QUALITY),
            random.choice(COMPOSITION),
            random.choice(CAMERA)
        ]

        prompt = ", ".join(dict.fromkeys(parts))
        metadata = f"(prompt_id: {seed}, style: {style})"
        full_prompt = prompt + f", compliant with Adobe Stock quality guidelines. {metadata}"

        if not dedupe or not is_duplicate(full_prompt):
            save_prompt_log(full_prompt)
            return {
                "prompt": full_prompt,
                "keywords": sorted(list(set(prompt.lower().replace(',', '').split()))),
                "seed": seed,
                "style": style
            }
        else:
            seed += 1

    raise RuntimeError("중복 회피 실패: 고유한 프롬프트를 생성하지 못했습니다.")

def generate_batch_prompts(n: int, category: str = "business", style: str = "default") -> list:
    return [generate_prompt(category, style) for _ in range(n)]

def save_prompts_to_file(prompts: list, filepath: str, format: str = "jsonl"):
    with open(filepath, "w", encoding="utf-8") as f:
        if format == "jsonl":
            for p in prompts:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
        elif format == "csv":
            import csv
            keys = ["prompt", "keywords", "seed", "style"]
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for p in prompts:
                writer.writerow(p)
