#!/usr/bin/env python3
"""Parse session 13 whisper log and emit speaker-labelled transcript."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SEG_RE = re.compile(r"^\[\s*(\d+(?:\.\d+)?)\]\s*(.+)$")

# Player table talk / cross-talk — keep as Table when no character signal.
CHAR_HINTS: list[tuple[str, list[str]]] = [
    ("Deathwalker", ["deathwalker", "door", "push the door", "barbarian", "goliath", "bean tea", "protein shake", "dw"]),
    ("Wilrin", ["wilrin", "mage hand", "sigil", "forge", "eyepatch", "sorcerer", "wild magic"]),
    ("Silrie", ["silrie", "meditation", "cult", "gillette", "quill", "reverat", "monk", "spiritual"]),
    ("Ros", ["ros", "panpipe", "pan pipe", "music", "ranger", "chicken", "critch"]),
    ("Pin", ["pin", "fighter", "locker", "anathemist", "eldritch knight"]),
    ("Amanira", ["amanira", "druid", "guidance", "tea", "perfect cup"]),
    ("Ayr", ["ayr", "paladin", "gnome", "journeyman", "righteousness"]),
]

GM_HINTS = (
    "roll ",
    "give me",
    "you find",
    "you walk",
    "you see",
    "okay, so",
    "as far as you",
    "the handwriting",
    "make a ",
    "what would you",
    "how would you",
    "insight",
    "persuasion",
    "investigation",
    "history",
    "dexterity",
    "strength",
    "wisdom",
    "intelligence",
    "she looks",
    "he looks",
    "bq).",
    "records office",
    "sable",
    "cedric",
    "katie",
)


def guess_speaker(text: str, prev: str | None) -> str:
    low = text.lower()
    if any(h in low for h in GM_HINTS) and not low.startswith(("i roll", "i got", "we roll", "that's a")):
        if any(x in low for x in ("you ", "your ", "roll ", "give me", "make a", "what do you", "how do you")):
            return "GM"
    if low.startswith(("i roll", "i got ", "can i ", "i want to", "i'm going to", "we should", "let's ")):
        scores: dict[str, int] = {}
        for name, hints in CHAR_HINTS:
            scores[name] = sum(1 for h in hints if h in low)
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            return best
        return "Table"
    for name, hints in CHAR_HINTS:
        if any(h in low for h in hints):
            return name
    if prev and prev not in ("GM", "Table", "Sable", "Cedric", "Katienaferu"):
        return prev
    return "Table"


def fmt_time(sec: float) -> str:
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def parse_log(path: Path) -> list[tuple[float, str]]:
    rows: list[tuple[float, str]] = []
    for line in path.read_text(errors="replace").splitlines():
        m = SEG_RE.match(line.strip())
        if m:
            rows.append((float(m.group(1)), m.group(2).strip()))
    return rows


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("notes/transcripts/session13_work/transcribe.log")
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("notes/transcripts/session_13.txt")

    rows = parse_log(src)
    if not rows:
        raise SystemExit(f"No segments parsed from {src}")

    lines = [
        "Session 13 transcript — The Lords of Sindrel",
        "In-game date: evening of the 31st of Enean, 4218 SC (continues from Session 12)",
        "",
        "Audio: dual table microphones aligned (~12.3 s offset); per-window best-source merge.",
        "Transcription: faster-whisper small.en. Speaker labels are heuristic (no diarization);",
        "GM = Benjamin; Table = unidentified cross-talk; character names = best-effort inference.",
        "",
        "---",
        "",
    ]

    prev = "GM"
    for t, text in rows:
        if not text:
            continue
        # NPC dialogue read by GM
        speaker = guess_speaker(text, prev)
        if "we had an arrangement" in text.lower() or "ask your questions" in text.lower():
            speaker = "Sable"
        if "welcome home" in text.lower() or "cedric" in text.lower() and "bin" in text.lower():
            speaker = "Cedric"
        if "destroy our door" in text.lower() or "investigators, you said" in text.lower():
            speaker = "Katienaferu"
        prev = speaker if speaker not in ("Sable", "Cedric", "Katienaferu") else prev
        lines.append(f"[{fmt_time(t)}] {speaker}: {text}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    print(f"Wrote {len(rows)} segments to {out}")


if __name__ == "__main__":
    main()
