#!/usr/bin/env python3
"""Build the three self-contained digital-human production pages from JSON on stdin."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from asset_references import validate_asset_references

TEMPLATE_NAMES = {
    "asset": "asset-inventory.template.html",
    "h3": "minimax-h3-shotlist.template.html",
    "list": "chinese-shotlist.template.html",
}

DIGITAL_HUMAN_RUNTIME = """<script id=\"digital-human-page-runtime\">(() => {
  const project = JSON.parse(document.getElementById('dh-project-data').textContent || '{}');
  if (project.package_mode !== 'digital_human') return;
  const shots = project.shots || [];
  const seconds = new Map(shots.map((shot) => [String(shot.id), Number(shot.seconds)]));
  for (const card of document.querySelectorAll('.shot')) {
    const id = card.id || card.querySelector('h2,h3')?.textContent.split('｜')[0];
    const value = seconds.get(String(id));
    const duration = card.querySelector('.duration');
    if (duration && Number.isFinite(value)) duration.textContent = `${value.toFixed(1)}秒`;
    const shot = shots.find((item) => String(item.id) === String(id));
    const role = card.querySelector('.role');
    if (role && shot?.voice_reference) {
      role.textContent = `讲者 / 出镜：${shot.performer || '画外音 / 插入画面'}　参考音色：${shot.voice_reference}（完整参考，不分段）`;
    }
  }
  const total = shots.reduce((sum, shot) => sum + (Number(shot.seconds) || 0), 0);
  document.querySelectorAll('.metrics .metric b').forEach((item) => {
    if (item.parentElement.textContent.includes('秒完整覆盖')) item.textContent = total.toFixed(1);
  });
  document.querySelectorAll('.audio-name').forEach((item) => item.closest('.panel')?.remove());
  document.querySelectorAll('.clip-play').forEach((item) => item.remove());
})();</script>"""


def safe_slug(value: str) -> str:
    value = re.sub(r"[<>:\\|?*/\"]", "_", value).strip()
    return value or "Video"


def build(template: Path, output: Path, project: dict) -> None:
    text = template.read_text(encoding="utf-8")
    payload = json.dumps(project, ensure_ascii=False).replace("</", "<\\/")
    marker = re.compile(
        r'(<script id="dh-project-data" type="application/json">)\s*\{\}\s*(</script>)',
        re.DOTALL,
    )
    if not marker.search(text):
        raise ValueError(f"Template data marker missing: {template}")
    rendered = marker.sub(
        lambda match: f"{match.group(1)}{payload}{match.group(2)}",
        text,
        count=1,
    )
    if project.get("package_mode") == "digital_human" and template.name != TEMPLATE_NAMES["asset"]:
        rendered = rendered.replace("</body>", f"{DIGITAL_HUMAN_RUNTIME}</body>")
    output.write_text(rendered, encoding="utf-8")


def read_project_data(source: str) -> dict:
    if source != "-":
        raise ValueError("Project data must be passed through stdin ('-'); do not create a project-manifest.json file.")
    raw = sys.stdin.read()
    if not raw.strip():
        raise ValueError("No project JSON received on stdin.")
    return json.loads(raw)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_data", help="Use '-' to read project JSON from stdin")
    parser.add_argument("output_dir", type=Path, help="Folder for the three HTML files")
    args = parser.parse_args()
    project = read_project_data(args.project_data)
    errors = validate_asset_references(project, args.output_dir)
    if errors:
        raise ValueError("Asset reference validation failed:\n" + "\n".join(errors))
    title = safe_slug(project.get("title", "MV"))
    root = Path(__file__).resolve().parents[1]
    templates = root / "assets" / "templates"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "asset": args.output_dir / f"{title}_GPT_Image2_资产清单.html",
        "h3": args.output_dir / f"{title}_MiniMaxH3_Shotlist.html",
        "list": args.output_dir / f"{title}_全中文分镜列表.html",
    }
    for key, output in outputs.items():
        build(templates / TEMPLATE_NAMES[key], output, project)
        print(output)


if __name__ == "__main__":
    main()
