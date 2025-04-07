import os
import torch
import soundfile as sf
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from g2pk import G2p

from resamplerate import resample_audio
from similarity import korean_similarity

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

model_path = "./whisper_step_output"
processor = WhisperProcessor.from_pretrained(model_path)
model = WhisperForConditionalGeneration.from_pretrained(model_path).to(
    "cuda" if torch.cuda.is_available() else "cpu"
)
device = model.device
g2p = G2p()

def get_pronunciation(text):
    """문장을 G2P로 발음 형태로 변환"""
    return ' '.join([g2p(word) for word in text.strip().split()])


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        text_input = request.form["text"]
        file = request.files["file"]

        if file and text_input:
            # ⬇️ 파일 저장 및 리샘플링
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp.wav")
            output_path = os.path.join(app.config["UPLOAD_FOLDER"], "converted.wav")
            file.save(input_path)
            resample_audio(input_path, output_path)

            # 🎧 오디오 로드 및 Whisper 처리
            audio_data, _ = sf.read(output_path)
            input_features = processor(
                audio_data, sampling_rate=16000, return_tensors="pt"
            ).input_features.to(device)

            predicted_ids = model.generate(input_features)
            transcription = processor.tokenizer.batch_decode(
                predicted_ids, skip_special_tokens=True
            )[0]

            # 📖 발음 추출
            input_pron = get_pronunciation(text_input)
            stt_pron = get_pronunciation(transcription)

            # 🎯 유사도 계산
            similarity = korean_similarity(input_pron, stt_pron)

            # 📦 결과 저장
            result = {
                "original_text": text_input,
                "original_pron": input_pron,
                "stt_text": transcription,
                "stt_pron": stt_pron,
                "similarity": similarity
            }

            # 🧹 임시파일 정리
            os.remove(input_path)
            os.remove(output_path)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
