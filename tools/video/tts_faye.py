#!/usr/bin/env python3
"""segments.yaml의 tts 문장을 페이 목소리(고정 기준 음성 복제)로 만든다.
사용법: python tts_faye.py <segments.yaml>
"""
import json
import sys
from pathlib import Path

import soundfile as sf
import torch
import yaml
from qwen_tts import Qwen3TTSModel


def main():
    data = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    ref_wav = Path(data["voice_ref"])
    ref_text = (ref_wav.parent / "ref_text.txt").read_text(encoding="utf-8").strip()
    out_dir = Path(data["media_root"]) / "3_voice"
    out_dir.mkdir(parents=True, exist_ok=True)

    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        device_map="cuda:0",
        dtype=torch.bfloat16,
    )
    prompt = model.create_voice_clone_prompt(ref_audio=str(ref_wav), ref_text=ref_text)

    report = []
    for s in data["segments"]:
        wavs, sr = model.generate_voice_clone(
            text=s["tts"], language="Korean", voice_clone_prompt=prompt)
        out = out_dir / f"{s['id']}.wav"
        sf.write(str(out), wavs[0], sr)
        dur = len(wavs[0]) / sr
        slot = round(s["end"] - s["start"], 2) if s["part"] == "body" else None
        over = " ← 구간보다 김" if slot and dur > slot else ""
        info = f" / 구간 {slot:5.1f}s{over}" if slot else ""
        print(f"{s['id']:6} 음성 {dur:5.1f}s{info}")
        report.append({"id": s["id"], "part": s["part"],
                       "voice_sec": round(dur, 2), "slot_sec": slot})

    (out_dir / "voice_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n완료: {out_dir}")


if __name__ == "__main__":
    main()