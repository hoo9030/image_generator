import random

# 프롬프트 구성 요소 풀
subjects = [
    "a misty forest", "a futuristic cityscape", "a glowing temple",
    "a surreal desert with floating rocks", "an abstract mountain made of glass"
]

lightings = [
    "cinematic lighting", "soft morning light", "neon backlight",
    "sunset glow", "diffused rim lighting"
]

camera_angles = [
    "wide-angle shot", "top-down view", "macro perspective",
    "aerial view", "85mm lens close-up"
]

styles = [
    "photorealistic", "ultra detailed", "dreamlike clarity",
    "clean composition", "8k textures"
]

emotions = [
    "ethereal mood", "mysterious feeling", "tranquil atmosphere",
    "majestic energy", "minimalist emotion"
]

def generate_prompt():
    subject = random.choice(subjects)
    lighting = random.choice(lightings)
    angle = random.choice(camera_angles)
    style = random.choice(styles)
    emotion = random.choice(emotions)

    prompt = f"{subject}, {lighting}, {angle}, {emotion}, {style}, high quality"
    return prompt
