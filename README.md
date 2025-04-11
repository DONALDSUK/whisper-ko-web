# 🗣️ Whisper Pronouncer KR

한국어 발음 교정을 위한 Whisper 기반 웹 애플리케이션입니다.  
사용자가 직접 음성 파일을 업로드하고 입력 문장을 비교하여 발음을 평가할 수 있습니다.

---

## 🔧 프로젝트 구성

- **모델**: [Whisper-small fine-tuned on KSS dataset](https://huggingface.co/donaldsuk/whisper-ko)
- **프레임워크**: Flask + PyTorch + Hugging Face Transformers
- **기능**
  - WAV 파일 업로드
  - STT 결과 생성 (Whisper fine-tuned 모델 사용)
  - 입력 문장과 STT 결과의 발음을 `g2pk`로 변환 및 비교

---

## 📂 사용법

### 1. 모델 다운로드

[➡️ Hugging Face 모델 바로가기](https://huggingface.co/donaldsuk/whisper-ko)

모델 파일을 다운받아 **`whisper_step_output/`** 폴더에 넣고 프로젝트 루트에 위치시켜주세요:

```
your-project-folder/
├── app.py
├── resamplate.py
├── similarity.py
├── whisper_step_output/     👈 모델 다운로드 후 여기에 넣기
│   ├── config.json
│   ├── preprocessor_config.json
│   ├── pytorch_model.bin
│   └── tokenizer_config.json
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 웹 실행

```bash
python app.py
```


## 📦 주요 라이브러리

- `transformers`
- `torch`
- `flask`
- `g2pk`
- `librosa`

---

## 🧠 모델 성능

- **WER**: 약 2.8%
- **학습 데이터**: KSS (발음 기반 G2P 라벨 전처리)
- **훈련 방식**: Whisper-small fine-tuning, step 기반 학습

---

## 🧪 테스트 추천 문장

- "밥솥이 터질 뻔했어"
- "읽다와 일다의 차이를 알아?"
- "닭과 달걀은 비슷하게 생겼지만 다르다"

---

## 👤 개발자

- Hugging Face: [donaldsuk](https://huggingface.co/donaldsuk)
- GitHub: [github.com/donaldsuk](https://github.com/donaldsuk)

---
