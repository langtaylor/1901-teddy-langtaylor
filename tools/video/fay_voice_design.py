#!/usr/bin/env python3
"""페이 목소리 후보 3개를 만든다 (Qwen3-TTS VoiceDesign)."""
from pathlib import Path

import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

OUT = Path("/mnt/c/Users/taylo/Videos/assets/characters/fay-smith/voice")
REF_TEXT = "자, 잘 들어요. 이건 제가 직접 뜯어보고 고친 거라 확실해요. 딱 두 가지만 기억하면 돼요."
INSTRUCT = (
    "Korean female, 25 years old, a confident and stubborn young engineer. "
    "Clear, crisp, slightly bright mid-high pitch. Fast, energetic pace. "
    "Assertive and decisive with a cheeky, teasing edge. Not soft, not shy, not calm."
)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
        device_map="cuda:0",
        dtype=torch.bfloat16,
    )
    (OUT / "ref_text.txt").write_text(REF_TEXT, encoding="utf-8")
    for i in range(1, 4):
        wavs, sr = model.generate_voice_design(
            text=REF_TEXT, language="Korean", instruct=INSTRUCT)
        p = OUT / f"candidate_{i}.wav"
        sf.write(str(p), wavs[0], sr)
        print("저장:", p)


if __name__ == "__main__":
    main()