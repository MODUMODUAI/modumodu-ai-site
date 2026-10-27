# -*- coding: utf-8 -*-
"""익명화 PNG로 약 15초 히어로 슬라이드 영상 생성."""
from pathlib import Path
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np

OUT = Path(__file__).resolve().parent
FINAL_WEBM = OUT / "hero-demo.webm"
FINAL_MP4 = OUT / "hero-demo.mp4"
W, H = 1440, 900
FPS = 30
TOTAL_SEC = 15

# 이미 샘플 데이터로 찍힌 화면
SLIDES = [
    "01-products.png",
    "02-orders.png",
    "03-inquiries.png",
    "06-wholesalers.png",
    "04-ownerclan.png",
    "05-settings.png",
]


def fit(img: np.ndarray) -> np.ndarray:
    canvas = np.full((H, W, 3), (245, 247, 250), dtype=np.uint8)
    h, w = img.shape[:2]
    scale = min(W / w, H / h)
    nw, nh = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)
    x = (W - nw) // 2
    y = (H - nh) // 2
    canvas[y : y + nh, x : x + nw] = resized
    return canvas


def main() -> None:
    frames_per = max(1, (TOTAL_SEC * FPS) // len(SLIDES))
    fade = max(4, FPS // 5)
    clips = []
    for name in SLIDES:
        path = OUT / name
        if not path.exists():
            raise SystemExit(f"missing {name}")
        img = cv2.imread(str(path))
        if img is None:
            raise SystemExit(f"read fail {name}")
        clips.append(fit(img))

    seq = []
    for i, frame in enumerate(clips):
        hold = frames_per - fade
        for _ in range(max(1, hold)):
            seq.append(frame)
        nxt = clips[(i + 1) % len(clips)]
        for k in range(fade):
            a = (k + 1) / (fade + 1)
            blended = cv2.addWeighted(frame, 1 - a, nxt, a, 0)
            seq.append(blended)

    seq = seq[: TOTAL_SEC * FPS]
    while len(seq) < TOTAL_SEC * FPS:
        seq.append(clips[-1])

    tmp_mp4 = OUT / "_hero_slide_tmp.mp4"
    writer = cv2.VideoWriter(str(tmp_mp4), cv2.VideoWriter_fourcc(*"mp4v"), FPS, (W, H))
    for frame in seq:
        writer.write(frame)
    writer.release()

    ff = imageio_ffmpeg.get_ffmpeg_exe()
    # 브라우저용 webm
    subprocess.run(
        [
            ff, "-y", "-i", str(tmp_mp4),
            "-c:v", "libvpx", "-b:v", "1.8M", "-an",
            str(FINAL_WEBM),
        ],
        capture_output=True,
        check=False,
    )
    # mp4 백업(호환)
    subprocess.run(
        [
            ff, "-y", "-i", str(tmp_mp4),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
            str(FINAL_MP4),
        ],
        capture_output=True,
        check=False,
    )
    tmp_mp4.unlink(missing_ok=True)
    print("webm", FINAL_WEBM.stat().st_size if FINAL_WEBM.exists() else 0)
    print("mp4", FINAL_MP4.stat().st_size if FINAL_MP4.exists() else 0)
    print("frames", len(seq), "sec", round(len(seq) / FPS, 1))


if __name__ == "__main__":
    main()
