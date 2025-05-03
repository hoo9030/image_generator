# 🧠 image_generator

AI 기반으로 Adobe Stock 수익화를 목표로 하는 자동 이미지 생성 시스템입니다.
Stable Diffusion WebUI를 기반으로 전체 루프가 자동화되어 있습니다.

---

## ✅ 주요 기능

- 프롬프트 자동 생성 (수익+품질 최적화)
- 품질 기준 사전 판단 및 필터링 (AI 거절 방지)
- 고해상도 이미지 생성 (WebUI API 연동)
- 메타데이터 자동 생성 (AI 생성 명시 포함)
- Adobe Stock 자동 업로드 (Selenium)
- 판매 피드백 기반 재생성 루프 예정

---

## 📦 설치 방법 (로컬)

1. Stable Diffusion WebUI 설치 (AUTOMATIC1111)
2. 모델 파일(sd-v1-5.ckpt 등)을 `/models/Stable-diffusion/`에 배치
3. `webui-user.bat` 파일에 `--api` 옵션 추가

```bat
set COMMANDLINE_ARGS=--api
```

4. `pip install -r requirements.txt`로 필요한 패키지 설치

---

## 🚀 실행 방법

```bash
python run_all.py
```

> 프롬프트 생성 → 이미지 생성 → 품질 필터 → 메타데이터 → 업로드 까지 자동 처리됩니다.

---

## 🗂️ 폴더 구조

```bash
outputs/
├── raw/         # 원본 이미지
├── passed/      # 통과 이미지 (업로드 대상)
├── rejected/    # 필터 실패
├── uploaded/    # 업로드 완료
├── thumbnails/  # 선택사항
```

---

## 📜 라이선스 / 사용 권장
- 생성 이미지는 "AI generated"로 반드시 명시되며, 스톡 플랫폼의 가이드라인을 따릅니다.
- 해당 시스템은 교육/연구/실제 수익화 목적 모두에 사용 가능합니다.

---

**Made for professional AI-based passive income.**
