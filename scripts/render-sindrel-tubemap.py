#!/usr/bin/env python3
"""Render Sindrel locations tubemap at campaign-friendly size."""
from pathlib import Path

from tubemap import parse_file, render

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "assets/maps/sindrel-locations.tubemap"
OUTPUT = ROOT / "assets/maps/sindrel-locations-tubemap.png"

spec = parse_file(INPUT)
render(
    spec,
    output=str(OUTPUT),
    title="Sindrel — Locations (Sessions 1–12)",
    figsize=(20, 14),
    dpi=200,
)
