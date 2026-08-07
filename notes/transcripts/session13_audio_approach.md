# Session 13 — dual-microphone handling

## Sources

| File | Format | Duration | Notes |
|------|--------|----------|-------|
| `The Lords of Sindrel Session 13.mp3` | mono 16 kHz | ~3h 12m | Table mic A |
| `2026-07-22-18-54-25.WAV` | stereo 16 kHz | ~3h 12m | Table mic B (L/R identical; duplicated mono) |

## Decision: align + best-source switching (not stack)

**Rejected: amplitude stacking / averaging.** Opposite-end table mics capture different speakers; summing aligned tracks causes phase cancellation and comb filtering.

**Rejected: simple “use MP3 only”.** Each mic favours the players nearest it; discarding one loses clarity on half the table.

**Chosen:** Cross-correlate the two mono tracks, trim to common length, then for each ~50 ms window pick the sample from whichever source has higher RMS energy. This is adaptive source switching without brittle hard cuts.

## Alignment

Cross-correlation on downsampled opening ~2 min:

- **Offset:** WAV leads MP3 by **12.30 s** (MP3 starts later).
- Merged duration: **11,555.9 s** (~3h 12m).

Merged audio: `session13_work/session13_merged.wav`

## Transcription

- Engine: faster-whisper `small.en`, CPU, VAD filter
- Output: `session13_work/transcribe.log` (5095 segments)
- Formatted transcript: `session_13.txt`
- **Speaker labels:** heuristic only (no diarization). `[GM]`, character names when inferable, `[Table]` for cross-talk. Wilrin and Pin are different players (two Jacks at the table); labels still cannot reliably map utterances to individual voices without diarization.

## Re-run

```bash
python3 scripts/session13_audio.py \
  "/path/to/Session 13.mp3" \
  "/path/to/2026-07-22-18-54-25.WAV" \
  --out-dir notes/transcripts/session13_work

# Transcription only (after merge):
python3 scripts/session13_audio.py ... --transcribe --model small.en
```
