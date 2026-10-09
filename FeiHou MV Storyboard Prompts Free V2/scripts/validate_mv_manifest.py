#!/usr/bin/env python3
"""Validate the production manifest invariants that affect H3 pages."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RANGE = re.compile(r"^\d{2}:\d{2}:\d{3}–\d{2}:\d{2}:\d{3}$")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors: list[str] = []
    seen: set[str] = set()
    asset_rows = data.get("assets", [])
    assets = {item.get("id") for item in asset_rows}
    audio_references = data.get("audio_references", [])
    for item in asset_rows:
        asset_id = item.get("id", "unnamed asset")
        if item.get("kind", "locked") not in {"locked", "provided"}:
            errors.append(f"{asset_id}: Free edition accepts supplied assets only; use kind locked or provided")
        if item.get("prompt_en") or item.get("prompt_zh"):
            errors.append(f"{asset_id}: Free edition does not accept asset-image generation prompts")
    for index, shot in enumerate(data.get("shots", []), 1):
        label = shot.get("id", f"shot {index}")
        if label in seen:
            errors.append(f"duplicate shot id: {label}")
        seen.add(label)
        if not RANGE.fullmatch(shot.get("range", "")):
            errors.append(f"{label}: range must use MM:SS:ddd–MM:SS:ddd")
        refs = shot.get("references", [])
        if len(refs) > 9:
            errors.append(f"{label}: {len(refs)} visual references exceed H3's 9-image cap")
        unknown = [ref for ref in refs if ref not in assets]
        if unknown:
            errors.append(f"{label}: unknown asset IDs: {', '.join(unknown)}")
        if not shot.get("lyrics"):
            errors.append(f"{label}: provide lyrics or the exact text 本段无歌词")
        for field in ("prompt_en", "prompt_zh", "camera", "scene", "action", "continuity"):
            if not shot.get(field):
                errors.append(f"{label}: missing {field}")
        for audio in audio_references:
            audio_label = audio.get("h3_label", "<Audio 1>")
            prompt = shot.get("prompt_en", "")
            definitions = prompt.split("summary:", 1)[0]
            retention = prompt.split("retention_analysis:", 1)[-1].split("detailed_description:", 1)[0]
            if audio_label not in definitions:
                errors.append(f"{label}: {audio_label} must be defined in subject_definitions")
            if "audio reference" not in prompt.split("retention_analysis:", 1)[0].lower() and "audio reuse" not in prompt.split("retention_analysis:", 1)[0].lower():
                errors.append(f"{label}: summary must declare audio reference or audio reuse")
            if f"{audio_label}: reference" not in retention and f"{audio_label}: fully_copy" not in retention and f"{audio_label}: partially_copy" not in retention and f"{audio_label}: weak_reference" not in retention:
                errors.append(f"{label}: retention_analysis needs an official relationship for {audio_label}")
    if errors:
        print("Manifest validation failed:", *errors, sep="\n- ")
        sys.exit(1)
    print(f"Manifest valid: {len(data.get('assets', []))} assets, {len(data.get('shots', []))} shots")


if __name__ == "__main__":
    main()
