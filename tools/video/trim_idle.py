#!/usr/bin/env python3
"""멈춘 화면 구간을 자동으로 찾아 빨리감기한 영상을 만든다.
사용법: python3 trim_idle.py merged.mp4 trimmed.mp4
"""
import json, re, shutil, subprocess, sys
from pathlib import Path

NOISE = 0.003        # 화면 변화 허용치 (덜 줄면 0.008로 올림)
MIN_FREEZE = float(__import__("os").environ.get("MIN_FREEZE", "2.0"))
KEEP = 0.7           # 멈춘 구간 앞부분을 원래 속도로 남길 시간(초)
FAST_RATE = 8.0      # 기본 빨리감기 배율
OUT_MIN, OUT_MAX = 1.0, 3.0
FPS = 60

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def duration(p):
    return float(run(["ffprobe","-v","error","-show_entries","format=duration",
                      "-of","csv=p=0",str(p)], check=True).stdout.strip())

def detect_freezes(p, total):
    print("멈춘 구간 찾는 중...")
    err = run(["ffmpeg","-hide_banner","-i",str(p),"-map","0:v:0","-vf",
               f"freezedetect=n={NOISE}:d={MIN_FREEZE}","-f","null","-"]).stderr
    s = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", err)]
    e = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", err)]
    if len(e) < len(s): e.append(total)
    return list(zip(s, e))

def build_segments(freezes, total):
    segs, cur = [], 0.0
    for s, e in freezes:
        k = min(s + KEEP, e)
        if k > cur: segs.append((cur, k, 1.0))
        L = e - k
        if L > 0.05:
            out = min(max(L / FAST_RATE, OUT_MIN), OUT_MAX, L)
            segs.append((k, e, L / out))
        cur = max(cur, e)
    if total - cur > 0.05: segs.append((cur, total, 1.0))
    return segs

def pick_encoder():
    t = run(["ffmpeg","-hide_banner","-f","lavfi","-i","color=c=black:s=256x256:d=0.2",
             "-c:v","h264_nvenc","-f","null","-"])
    if t.returncode == 0:
        print("인코더: NVENC (GPU)")
        return ["-c:v","h264_nvenc","-preset","p5","-cq","20"]
    print("인코더: libx264 (CPU)")
    return ["-c:v","libx264","-preset","veryfast","-crf","18"]

def main():
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    total = duration(src)
    freezes = detect_freezes(src, total)
    segs = build_segments(freezes, total)
    enc = pick_encoder()
    tmp = dst.parent / f"_{dst.stem}_segments"
    shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
    report, t = [], 0.0
    for i, (s, e, sp) in enumerate(segs):
        part = tmp / f"seg{i:03d}.mp4"
        vf = f"setpts=PTS/{sp:.4f},fps={FPS}" if sp > 1.001 else f"fps={FPS}"
        print(f"[{i+1}/{len(segs)}] {s:7.2f}~{e:7.2f}s  x{sp:.1f}")
        run(["ffmpeg","-y","-hide_banner","-ss",f"{s:.3f}","-t",f"{e-s:.3f}",
             "-i",str(src),"-vf",vf,"-an",*enc,str(part)], check=True)
        n = (e - s) / sp
        report.append({"index":i,"src_start":round(s,2),"src_end":round(e,2),
                       "speed":round(sp,2),"out_start":round(t,2),"out_end":round(t+n,2)})
        t += n
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in sorted(tmp.glob("seg*.mp4"))))
    run(["ffmpeg","-y","-hide_banner","-f","concat","-safe","0","-i",str(lst),
         "-c","copy",str(dst)], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    seg_file = dst.with_suffix(".segments.json")
    seg_file.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\n완료: {dst}")
    print(f"원본 {total:.1f}초 → 결과 {t:.1f}초 (멈춘 구간 {len(freezes)}개 처리)")

if __name__ == "__main__":
    main()
