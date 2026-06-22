#!/usr/bin/env python3
"""Fold one 👍/👎 feedback issue into data/taste.json.

Reads two env vars (set by the feedback workflow):
  FEEDBACK_KIND : "like" or "dislike"
  ISSUE_BODY    : the issue body, which contains a line "tags: a, b, c"

A 'like' nudges each tag's weight up; a 'dislike' nudges it down. Weights
accumulate across votes, so repeated feedback steadily reshapes the digest.
The daily run reads this file and adjusts each item's score accordingly.
"""

import json
import os
import re
import sys
from pathlib import Path

TASTE = Path("data/taste.json")
LIKE_STEP = 1.0
DISLIKE_STEP = 1.5


def _clean(tag: str) -> str:
    return tag.strip().lstrip("#").lower()


def main() -> None:
    kind = os.environ.get("FEEDBACK_KIND", "").strip().lower()
    body = os.environ.get("ISSUE_BODY", "") or ""

    if kind not in ("like", "dislike"):
        print(f"Unknown feedback kind: {kind!r}; nothing to do.")
        return

    match = re.search(r"(?im)^\s*tags:\s*(.+)$", body)
    if not match:
        print("No 'tags:' line found in issue body; nothing to do.")
        return

    tags = [_clean(t) for t in match.group(1).split(",") if _clean(t)]
    if not tags:
        print("No tags parsed; nothing to do.")
        return

    data = {"boost": {}, "suppress": {}}
    if TASTE.exists():
        try:
            data = json.loads(TASTE.read_text(encoding="utf-8"))
        except Exception:
            pass
    data.setdefault("boost", {})
    data.setdefault("suppress", {})

    for tag in tags:
        if kind == "like":
            data["boost"][tag] = round(float(data["boost"].get(tag, 0.0)) + LIKE_STEP, 2)
            # ease any prior suppression of the same tag
            if tag in data["suppress"]:
                eased = round(min(0.0, float(data["suppress"][tag]) + LIKE_STEP), 2)
                if eased == 0.0:
                    del data["suppress"][tag]
                else:
                    data["suppress"][tag] = eased
        else:
            data["suppress"][tag] = round(float(data["suppress"].get(tag, 0.0)) - DISLIKE_STEP, 2)
            # ease any prior boost of the same tag
            if tag in data["boost"]:
                eased = round(max(0.0, float(data["boost"][tag]) - DISLIKE_STEP), 2)
                if eased == 0.0:
                    del data["boost"][tag]
                else:
                    data["boost"][tag] = eased

    TASTE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Applied {kind} to tags: {tags}")


if __name__ == "__main__":
    main()
    sys.exit(0)
