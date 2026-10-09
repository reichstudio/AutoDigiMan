#!/usr/bin/env python3
"""Recursively extract readable project documents to JSON without modifying them.

The result is source material for a human/AI review step. It deliberately does
not decide that arbitrary document text is an executable instruction.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
import re
import sys
import zipfile
from xml.etree import ElementTree as ET


TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".csv", ".json", ".yaml", ".yml", ".html", ".htm", ".xml"}
SUPPORTED_EXTENSIONS = TEXT_EXTENSIONS | {".rtf", ".docx", ".odt", ".pdf", ".xlsx", ".xlsm", ".pptx"}
LEGACY_OR_UNSUPPORTED = {".doc", ".xls", ".ppt"}
IGNORED_DIRECTORIES = {".git", ".svn", "node_modules", "__pycache__"}


def clean_text(value: str) -> str:
    value = html.unescape(value).replace("\xa0", " ")
    value = re.sub(r"\r\n?", "\n", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def read_plain(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-16", "gb18030", "latin-1"):
        try:
            return clean_text(raw.decode(encoding))
        except UnicodeDecodeError:
            continue
    raise ValueError("无法解码文本")


def xml_text(data: bytes, *, break_tag: str | None = None) -> str:
    root = ET.fromstring(data)
    output: list[str] = []
    for element in root.iter():
        if element.text:
            output.append(element.text)
        if break_tag and element.tag.endswith(break_tag):
            output.append("\n")
    return clean_text("".join(output))


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        names = ["word/document.xml"]
        names.extend(name for name in archive.namelist() if name.startswith("word/header") or name.startswith("word/footer"))
        parts = [xml_text(archive.read(name), break_tag="}p") for name in names if name in archive.namelist()]
    return clean_text("\n".join(part for part in parts if part))


def read_odt(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return xml_text(archive.read("content.xml"), break_tag="}p")


def read_pptx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        names = sorted(name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name))
        return clean_text("\n".join(xml_text(archive.read(name)) for name in names))


def read_xlsx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = [clean_text("".join(item.itertext())) for item in shared_root]
        values: list[str] = []
        names = sorted(name for name in archive.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", name))
        for name in names:
            root = ET.fromstring(archive.read(name))
            for cell in root.iter():
                if not cell.tag.endswith("}c"):
                    continue
                cell_type = cell.attrib.get("t")
                value = next((node.text or "" for node in cell if node.tag.endswith("}v")), "")
                if cell_type == "s" and value.isdigit() and int(value) < len(shared):
                    value = shared[int(value)]
                elif cell_type == "inlineStr":
                    value = clean_text("".join(cell.itertext()))
                if value:
                    values.append(value)
    return clean_text("\n".join(values))


def read_rtf(path: Path) -> str:
    raw = read_plain(path)
    raw = re.sub(r"\\par[d]?", "\n", raw)
    raw = re.sub(r"\\'[0-9a-fA-F]{2}", "", raw)
    raw = re.sub(r"\\[a-zA-Z]+-?\d* ?", "", raw)
    return clean_text(raw.replace("{", "").replace("}", ""))


def read_pdf(path: Path) -> str:
    try:
        import fitz  # PyMuPDF

        document = fitz.open(path)
        return clean_text("\n".join(page.get_text("text") for page in document))
    except ImportError:
        try:
            from pypdf import PdfReader

            return clean_text("\n".join(page.extract_text() or "" for page in PdfReader(path).pages))
        except ImportError as error:
            raise ValueError("当前环境缺少 PDF 文本提取器（PyMuPDF 或 pypdf）") from error


def extract(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTENSIONS:
        return read_plain(path)
    if suffix == ".rtf":
        return read_rtf(path)
    if suffix == ".docx":
        return read_docx(path)
    if suffix == ".odt":
        return read_odt(path)
    if suffix in {".xlsx", ".xlsm"}:
        return read_xlsx(path)
    if suffix == ".pptx":
        return read_pptx(path)
    if suffix == ".pdf":
        return read_pdf(path)
    raise ValueError("不支持的文档格式")


def headings(text: str) -> list[str]:
    return [line.strip("#* -\t") for line in text.splitlines() if re.match(r"^\s*(?:#{1,6}\s+|[一二三四五六七八九十]+[、.．]\s*|\d+[、.．]\s*)", line)][:80]


def likely_content(text: str) -> list[str]:
    result: list[str] = []
    lowered = text.lower()
    if re.search(r"制作要求|项目要求|视频要求|画面要求|风格|场景|人物|受众|时长|画幅|禁忌|必须", text):
        result.append("production_requirements_candidate")
    if re.search(r"口播|台词|旁白|脚本|逐字稿|speak|voiceover", lowered, re.IGNORECASE):
        result.append("speech_candidate")
    return result or ["needs_content_review"]


def candidate_files(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue
        if path.suffix.lower() in SUPPORTED_EXTENSIONS | LEGACY_OR_UNSUPPORTED:
            candidates.append(path)
    return sorted(candidates, key=lambda item: str(item).lower())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="Project/material folder to scan recursively")
    parser.add_argument("--max-file-mib", type=float, default=30, help="Skip files larger than this size (default: 30)")
    args = parser.parse_args()
    root = args.folder.resolve()
    if not root.is_dir():
        parser.error(f"Not a folder: {root}")
    limit = int(args.max_file_mib * 1024 * 1024)
    documents: list[dict[str, object]] = []
    for path in candidate_files(root):
        relative = path.relative_to(root).as_posix()
        item: dict[str, object] = {"path": relative, "extension": path.suffix.lower()}
        if path.suffix.lower() in LEGACY_OR_UNSUPPORTED:
            item.update(status="unreadable", reason="旧版格式，请转换为 .docx、.xlsx、.pptx 或 .pdf 后重新扫描")
        elif path.stat().st_size > limit:
            item.update(status="unreadable", reason=f"文件超过 {args.max_file_mib:g} MiB 扫描上限")
        else:
            try:
                text = extract(path)
                item.update(status="readable", characters=len(text), headings=headings(text), likely_content=likely_content(text), text=text)
            except (OSError, ValueError, ET.ParseError, zipfile.BadZipFile) as error:
                item.update(status="unreadable", reason=str(error))
        documents.append(item)
    print(json.dumps({"root": str(root), "documents": documents}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
