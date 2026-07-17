#!/usr/bin/env python3
"""Lore dashboard now lives on the lore bridge service.

Open https://obsidianportal-git-sync.onrender.com/ (HTML) after deploy.
Generator source: obsidianportal-git-sync/src/lore_bridge/dashboard.py
"""

from __future__ import annotations

import sys

URL = "https://obsidianportal-git-sync.onrender.com/"


def main() -> None:
    print(f"Lore dashboard is served by the bridge: {URL}")
    print("See obsidianportal-git-sync/src/lore_bridge/dashboard.py")
    sys.exit(0)


if __name__ == "__main__":
    main()
