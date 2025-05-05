# image_runner.py — 공통 이미지 생성 설정 모듈

def get_image_config(style: str = "default") -> dict:
    config_map = {
        "default":  {"steps": 30, "cfg_scale": 7.0, "sampler_index": "DPM++ 2M Karras"},
        "minimal":  {"steps": 25, "cfg_scale": 6.5, "sampler_index": "DPM++ SDE Karras"},
        "premium":  {"steps": 35, "cfg_scale": 8.5, "sampler_index": "DPM++ 2M SDE Karras"},
        "casual":   {"steps": 28, "cfg_scale": 6.0, "sampler_index": "Euler a"},
    }
    return config_map.get(style, config_map["default"])

def get_default_dimensions() -> tuple:
    return (2560, 1600)

def get_default_flags() -> dict:
    return {
        "enable_hr": True,
        "enable_tiled_vae": True
    }
