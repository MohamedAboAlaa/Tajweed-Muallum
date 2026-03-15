import whisperx
import json
import os
import torch
import librosa
from pathlib import Path
from tqdm import tqdm

QURAN_DB_PATH = "Quran_Database"
OUTPUT_JSON   = "quran_timestamps.json"
DEVICE        = "cuda" if torch.cuda.is_available() else "cpu"
COMPUTE_TYPE  = "float16" if torch.cuda.is_available() else "int8"

print(f"Device: {DEVICE}")
print(f"Quran DB: {QURAN_DB_PATH}")

print("Loading alignment model...")
model_a, metadata = whisperx.load_align_model(language_code="ar", device=DEVICE)
print("Model is ready!")


def process_aya(audio_path, text):
    try:
        audio    = whisperx.load_audio(str(audio_path))
        duration = librosa.get_duration(path=str(audio_path))

        segments = [{"text": text, "start": 0.0, "end": duration}]

        result = whisperx.align(
            segments, model_a, metadata, audio, DEVICE,
            return_char_alignments=False
        )

        words = []
        for segment in result["segments"]:
            if "words" in segment:
                for w in segment["words"]:
                    if "start" in w and "end" in w:
                        words.append({
                            "word" : w["word"].strip(),
                            "start": round(w["start"], 3),
                            "end"  : round(w["end"],   3),
                            "score": round(w.get("score", 0), 3),
                        })
        return words

    except Exception as e:
        print(f"Error in {audio_path.name}: {e}")
        return []


if os.path.exists(OUTPUT_JSON):
    with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
        quran_data = json.load(f)
    print(f"Resuming from checkpoint: {len(quran_data)} surahs done")
else:
    quran_data = {}

surah_dirs = sorted(Path(QURAN_DB_PATH).iterdir())

for surah_dir in tqdm(surah_dirs, desc="Surah"):
    if not surah_dir.is_dir():
        continue

    parts      = surah_dir.name.split("_", 1)
    surah_num  = parts[0]
    surah_name = parts[1] if len(parts) > 1 else surah_dir.name

    if surah_num in quran_data:
        print(f"Skipping {surah_num} — already done")
        continue

    print(f"\nSurah {surah_num} — {surah_name}")

    quran_data[surah_num] = {
        "surah_number": int(surah_num),
        "surah_name"  : surah_name,
        "ayat"        : {}
    }

    audio_files = sorted(surah_dir.glob("*.mp3"))

    for audio_file in tqdm(audio_files, desc=f"Ayas {surah_num}", leave=False):
        aya_num  = audio_file.stem
        txt_file = audio_file.with_suffix(".txt")

        if not txt_file.exists():
            print(f"No text file for aya {aya_num}")
            continue

        with open(txt_file, "r", encoding="utf-8") as f:
            aya_text = f.read().strip()

        print(f"Aya {aya_num}: {aya_text[:50]}...")

        words = process_aya(audio_file, aya_text)

        quran_data[surah_num]["ayat"][aya_num] = {
            "aya_number": int(aya_num),
            "text"      : aya_text,
            "words"     : words
        }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(quran_data, f, ensure_ascii=False, indent=2)
    print(f"Saved surah {surah_num}")


with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(quran_data, f, ensure_ascii=False, indent=2)

print(f"\nDone: {OUTPUT_JSON}")

total_ayat  = sum(len(s["ayat"]) for s in quran_data.values())
total_words = sum(
    len(a["words"])
    for s in quran_data.values()
    for a in s["ayat"].values()
)
print(f"Surahs : {len(quran_data)}")
print(f"Ayas   : {total_ayat:,}")
print(f"Words  : {total_words:,}")