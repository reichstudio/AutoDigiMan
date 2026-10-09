#!/usr/bin/env python3
"""Build the three self-contained MV production pages from one manifest JSON."""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

TEMPLATE_NAMES = {
    "asset": "reference-inventory.template.html",
    "h3": "minimax-h3-shotlist.template.html",
    "list": "chinese-shotlist.template.html",
}


def safe_slug(value: str) -> str:
    value = re.sub(r"[<>:\\|?*/\"]", "_", value).strip()
    return value or "MV"


def build(template: Path, output: Path, project: dict) -> None:
    text = template.read_text(encoding="utf-8")
    payload = json.dumps(project, ensure_ascii=False).replace("</", "<\\/")
    marker = '<script id="mv-project-data" type="application/json">{}</script>'
    if marker not in text:
        raise ValueError(f"Template data marker missing: {template}")
    output.write_text(text.replace(marker, f'<script id="mv-project-data" type="application/json">{payload}</script>'), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Project manifest JSON")
    parser.add_argument("output_dir", type=Path, help="Folder for the three HTML files")
    args = parser.parse_args()
    project = json.loads(args.manifest.read_text(encoding="utf-8"))
    title = safe_slug(project.get("title", "MV"))
    root = Path(__file__).resolve().parents[1]
    templates = root / "assets" / "templates"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "asset": args.output_dir / f"{title}_参考图片清单.html",
        "h3": args.output_dir / f"{title}_MiniMaxH3_Shotlist.html",
        "list": args.output_dir / f"{title}_全中文分镜列表.html",
    }
    for key, output in outputs.items():
        build(templates / TEMPLATE_NAMES[key], output, project)
        print(output)


if __name__ == "__main__":
    main()
