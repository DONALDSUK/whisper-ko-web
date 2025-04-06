# resamplerate.py
import torchaudio
import soundfile as sf
import os
import sys

def resample_audio(input_path, output_path, target_sr=16000):
    # 오디오 로드
    waveform, sample_rate = torchaudio.load(input_path)

    # 리샘플링 필요 여부 확인
    if sample_rate != target_sr:
        print(f"🔁 샘플링 레이트 변환 중: {sample_rate}Hz → {target_sr}Hz")
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sr)
        resampled = resampler(waveform)
    else:
        print(f"✅ 이미 {target_sr}Hz입니다. 그대로 복사합니다.")
        resampled = waveform

    # 저장 (WAV 포맷)
    torchaudio.save(output_path, resampled, sample_rate=target_sr)
    print(f"📁 저장 완료 → {output_path}")

# CLI로 사용 가능하게
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❗ 사용법: python resamplerate.py <입력파일> <출력파일>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print("❌ 입력 파일이 존재하지 않습니다.")
        sys.exit(1)

    resample_audio(input_file, output_file)
