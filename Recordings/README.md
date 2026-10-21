# Session recordings layout

Each processed session lives under `Recordings/session-<N>/`:

```
session-<N>/
  session.toml              # pipeline config (paths relative to this folder)
  session-<N>-primary.json  # canonical ASR transcript (segments with start/end/text)
  raw_inputs/
    recordings/             # source and reference audio (mp3, wav)
    *.txt                   # Plaud transcript exports and summary/notes
  processing/
    report.json             # last run metadata; points at primary + outputs
    session-<N>.wav         # merged/normalised audio used for transcription
    session-<N>.mp3
    *_comparison.json       # optional Plaud vs primary alignment (when plaud_transcripts set)
```

**Use for lore work:** `session-<N>-primary.json` at the session root.

**Plaud `.txt` files** under `raw_inputs/` are reference only (speakers, readability). Cross-check via `processing/*_comparison.json` when present.

Re-run your audio pipeline with `session.toml` in the session folder; it expects the paths above.
