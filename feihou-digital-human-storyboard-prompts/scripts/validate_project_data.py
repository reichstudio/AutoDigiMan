#!/usr/bin/env python3
"""Validate the in-memory project-data invariants that affect H3 pages.

Read JSON from standard input only. This deliberately prevents a persisted
project-manifest.json from becoming part of a project or delivery package.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from asset_references import validate_asset_references

RANGE = re.compile(r"^\d{2}:\d{2}:\d{3}–\d{2}:\d{2}:\d{3}$")
ZERO_RANGE = "00:00:000–00:00:000"
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}


def validate_reference_files(errors: list[str], items: object, prefix: str, extensions: set[str]) -> None:
    if not isinstance(items, list):
        errors.append(f"{prefix.lower()}_references must be a list")
        return
    if len(items) > 3:
        errors.append(f"{prefix.lower()}_references supports at most 3 files")
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            errors.append(f"{prefix}{index}: reference must be an object")
            continue
        expected = f"{prefix}{index}"
        filename = str(item.get("file", ""))
        path = Path(filename)
        if item.get("id") != expected:
            errors.append(f"{prefix}{index}: id must be {expected}")
        if path.stem != expected or path.suffix.lower() not in extensions:
            allowed = ", ".join(sorted(extensions))
            errors.append(f"{prefix}{index}: file must be {expected} with a supported extension ({allowed})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_data", choices=["-"], help="Read project JSON from stdin")
    parser.add_argument("--asset-root", type=Path, help="Package directory for checking image files")
    args = parser.parse_args()
    raw = sys.stdin.read()
    if not raw.strip():
        print("Project-data validation failed:\n- no JSON received on stdin")
        sys.exit(1)
    data = json.loads(raw)
    errors: list[str] = validate_asset_references(data, args.asset_root)
    seen: set[str] = set()
    assets = {item.get("id") for item in data.get("assets", [])}
    audio_references = data.get("audio_references", [])
    video_references = data.get("video_references", [])
    digital_human = data.get("package_mode") == "digital_human"
    if digital_human and data.get("master_audio"):
        errors.append("digital-human packages must not declare master_audio")
    for audio in audio_references:
        if digital_human and audio.get("role") != "voice_timbre_reference":
            errors.append("digital-human audio_references only allow voice_timbre_reference")
    validate_reference_files(errors, audio_references, "A", AUDIO_EXTENSIONS)
    validate_reference_files(errors, video_references, "V", VIDEO_EXTENSIONS)
    for index, shot in enumerate(data.get("shots", []), 1):
        label = shot.get("id", f"shot {index}")
        if label in seen:
            errors.append(f"duplicate shot id: {label}")
        seen.add(label)
        if not RANGE.fullmatch(shot.get("range", "")):
            errors.append(f"{label}: range must use MM:SS:ddd–MM:SS:ddd")
        if digital_human:
            if shot.get("range") != ZERO_RANGE:
                errors.append(f"{label}: digital-human range must be {ZERO_RANGE}")
            try:
                seconds = float(shot["seconds"])
            except (KeyError, TypeError, ValueError):
                errors.append(f"{label}: digital-human shots require numeric seconds")
            else:
                if not 0.2 <= seconds <= 30:
                    errors.append(f"{label}: seconds must be within Easy H3's 0.2–30s range")
            if "audio_slice" in shot:
                errors.append(f"{label}: digital-human shots must not contain audio_slice")
        refs = shot.get("references", [])
        if len(refs) > 9:
            errors.append(f"{label}: {len(refs)} visual references exceed H3's 9-image cap")
        unknown = [ref for ref in refs if ref not in assets]
        if unknown:
            errors.append(f"{label}: unknown asset IDs: {', '.join(unknown)}")
        if not shot.get("speech"):
            errors.append(f"{label}: provide speech or the exact text 本段无口播")
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
        print("Project-data validation failed:", *errors, sep="\n- ")
        sys.exit(1)
    print(f"Project data valid: {len(data.get('assets', []))} assets, {len(data.get('shots', []))} shots")


if __name__ == "__main__":
    main()
