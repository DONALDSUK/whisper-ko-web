import os
import io
import torch
import soundfile as sf
from flask import Flask, request, render_template
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from g2pk import G2p
from werkzeug.utils import secure_filename

from resamplerate import resample_audio  # ✅ import

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# 모델 로드
model_path = "./whisper_step_output"
processor = WhisperProcessor.from_pretrained(model_path)
model = WhisperForConditionalGeneration.from_pretrained(model_path).to("cuda" if torch.cuda.is_available() else "cpu")
device = model.device

g2p = G2p()

def get_pronunciation(text):
    return ' '.join([g2p(w) for w in text.strip().split()])

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text_input = request.form["text"]
        file = request.files["file"]

        if file and text_input:
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp.wav")
            output_path = os.path.join(app.config["UPLOAD_FOLDER"], "converted.wav")
            file.save(input_path)

            # 🔁 샘플링 레이트 자동 변환
            resample_audio(input_path, output_path)

            # 오디오 로드
            audio_data, _ = sf.read(output_path)

            # Whisper 추론
            input_features = processor(audio_data, sampling_rate=16000, return_tensors="pt").input_features.to(device)
            predicted_ids = model.generate(input_features)
            transcription = processor.tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)[0]

            # 발음 추출
            input_pron = get_pronunciation(text_input)
            stt_pron = get_pronunciation(transcription)

            result = {
                "original_text": text_input,
                "original_pron": input_pron,
                "stt_text": transcription,
                "stt_pron": stt_pron
            }

            # (선택) 임시파일 삭제
            os.remove(input_path)
            os.remove(output_path)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
