#!/usr/bin/env python3
"""Align dual table-mic recordings, merge by per-window best SNR, transcribe."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from scipy import signal


def run_ffmpeg(args: list[str]) -> None:
    cmd = ["/opt/homebrew/bin/ffmpeg", "-y", *args]
    subprocess.run(cmd, check=True, capture_output=True)


def load_mono_wav(path: Path, sample_rate: int = 16000) -> np.ndarray:
    with tempfile.NamedTemporaryFile(suffix=".raw", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        run_ffmpeg(
            [
                "-i",
                str(path),
                "-ac",
                "1",
                "-ar",
                str(sample_rate),
                "-f",
                "s16le",
                str(tmp_path),
            ]
        )
        data = np.fromfile(tmp_path, dtype=np.int16).astype(np.float32) / 32768.0
    finally:
        tmp_path.unlink(missing_ok=True)
    return data


def load_stereo_channels(path: Path, sample_rate: int = 16000) -> tuple[np.ndarray, np.ndarray]:
    with tempfile.NamedTemporaryFile(suffix=".raw", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        run_ffmpeg(
            [
                "-i",
                str(path),
                "-ac",
                "2",
                "-ar",
                str(sample_rate),
                "-f",
                "s16le",
                str(tmp_path),
            ]
        )
        interleaved = np.fromfile(tmp_path, dtype=np.int16).astype(np.float32) / 32768.0
        left = interleaved[0::2].copy()
        right = interleaved[1::2].copy()
    finally:
        tmp_path.unlink(missing_ok=True)
    return left, right


def cross_correlate_offset(a: np.ndarray, b: np.ndarray, max_lag_sec: float = 30.0, sr: int = 16000) -> int:
    """Return sample offset: b should start at a[offset] (positive = b is delayed)."""
    max_lag = int(max_lag_sec * sr)
    # Use downsampled excerpt for speed
    step = 4
    a_ds = a[::step]
    b_ds = b[::step]
    n = min(len(a_ds), len(b_ds), sr * 120)  # first ~2 min
    corr = signal.correlate(a_ds[:n], b_ds[:n], mode="full")
    lags = signal.correlation_lags(len(a_ds[:n]), len(b_ds[:n]), mode="full")
    mask = (lags >= -max_lag // step) & (lags <= max_lag // step)
    best = lags[mask][np.argmax(corr[mask])]
    return int(best * step)


def rms_envelope(x: np.ndarray, window: int) -> np.ndarray:
    x2 = x.astype(np.float64) ** 2
    kernel = np.ones(window) / window
    return np.sqrt(np.convolve(x2, kernel, mode="same"))


def merge_best_source(sources: list[np.ndarray], sr: int = 16000, window_ms: int = 50) -> np.ndarray:
    """Pick loudest source per window (avoids phase cancellation from stacking)."""
    window = max(1, int(sr * window_ms / 1000))
    envs = [rms_envelope(s, window) for s in sources]
    stacked = np.stack(envs)
    best = np.argmax(stacked, axis=0)
    out = np.zeros_like(sources[0])
    for i, s in enumerate(sources):
        out[best == i] = s[best == i]
    return np.clip(out, -1.0, 1.0)


def save_wav(path: Path, data: np.ndarray, sr: int = 16000) -> None:
    pcm = (np.clip(data, -1.0, 1.0) * 32767).astype(np.int16)
    with tempfile.NamedTemporaryFile(suffix=".raw", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        pcm.tofile(tmp_path)
        run_ffmpeg(
            [
                "-f",
                "s16le",
                "-ar",
                str(sr),
                "-ac",
                "1",
                "-i",
                str(tmp_path),
                str(path),
            ]
        )
    finally:
        tmp_path.unlink(missing_ok=True)


def analyze_and_merge(mp3: Path, wav: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    sr = 16000

    mp3_data = load_mono_wav(mp3, sr)
    wav_l, wav_r = load_stereo_channels(wav, sr)

    # Check if L/R are independent mics or near-duplicate
    min_len = min(len(wav_l), len(wav_r))
    lr_corr = float(np.corrcoef(wav_l[:min_len], wav_r[:min_len])[0, 1])

    # Align mp3 vs wav left (representative channel)
    offset = cross_correlate_offset(mp3_data, wav_l)
    if offset > 0:
        mp3_aligned = mp3_data[offset:]
        wav_l_aligned = wav_l[: len(mp3_aligned)]
        wav_r_aligned = wav_r[: len(mp3_aligned)]
    else:
        shift = -offset
        wav_l_aligned = wav_l[shift:]
        wav_r_aligned = wav_r[shift:]
        mp3_aligned = mp3_data[: len(wav_l_aligned)]

    n = min(len(mp3_aligned), len(wav_l_aligned), len(wav_r_aligned))
    mp3_aligned = mp3_aligned[:n]
    wav_l_aligned = wav_l_aligned[:n]
    wav_r_aligned = wav_r_aligned[:n]

    merged = merge_best_source([mp3_aligned, wav_l_aligned, wav_r_aligned], sr)
    merged_path = out_dir / "session13_merged.wav"
    save_wav(merged_path, merged, sr)

    # Also export individual aligned sources for optional per-source transcription
    for name, data in [("mp3", mp3_aligned), ("wav_l", wav_l_aligned), ("wav_r", wav_r_aligned)]:
        save_wav(out_dir / f"session13_{name}_aligned.wav", data, sr)

    meta = {
        "approach": "align + per-window best-source selection (not amplitude stack)",
        "reason": "Opposite table mics: stacking causes phase issues; switching preserves clearest speaker per moment.",
        "mp3": str(mp3),
        "wav": str(wav),
        "sample_rate": sr,
        "duration_sec": n / sr,
        "cross_correlation_offset_samples": offset,
        "cross_correlation_offset_sec": offset / sr,
        "wav_stereo_correlation": lr_corr,
        "merged_wav": str(merged_path),
    }
    (out_dir / "session13_audio_meta.json").write_text(json.dumps(meta, indent=2))
    return meta


def transcribe(wav_path: Path, out_json: Path, model_size: str = "small.en") -> None:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(wav_path),
        beam_size=5,
        vad_filter=True,
        word_timestamps=False,
    )
    rows = []
    for seg in segments:
        rows.append(
            {
                "start": seg.start,
                "end": seg.end,
                "text": seg.text.strip(),
            }
        )
        print(f"[{seg.start:7.1f}] {seg.text.strip()}", flush=True)

    out_json.write_text(json.dumps({"language": info.language, "segments": rows}, indent=2))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("mp3")
    p.add_argument("wav")
    p.add_argument("--out-dir", default="notes/transcripts/session13_work")
    p.add_argument("--transcribe", action="store_true")
    p.add_argument("--model", default="small.en")
    args = p.parse_args()

    out_dir = Path(args.out_dir)
    meta = analyze_and_merge(Path(args.mp3), Path(args.wav), out_dir)
    print(json.dumps(meta, indent=2))

    if args.transcribe:
        transcribe(Path(meta["merged_wav"]), out_dir / "session13_raw.json", args.model)


if __name__ == "__main__":
    main()
