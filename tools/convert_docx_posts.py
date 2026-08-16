#!/usr/bin/env python3
"""Turn Word blog sources into the Markdown and image files the site already serves."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
IMAGE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"


def visible_text(element: ET.Element) -> str:
    parts = []
    for node in element.iter():
        if node.tag == W + "t":
            parts.append(node.text or "")
        elif node.tag == W + "tab":
            parts.append("\t")
        elif node.tag in {W + "br", W + "cr"}:
            parts.append("\n")
    return "".join(parts)


def relationships(document: zipfile.ZipFile) -> tuple[dict[str, str], dict[str, str]]:
    root = ET.fromstring(document.read("word/_rels/document.xml.rels"))
    targets = {item.get("Id"): item.get("Target") for item in root.findall(REL + "Relationship")}
    images = {
        item.get("Id"): item.get("Target")
        for item in root.findall(REL + "Relationship")
        if item.get("Type") == IMAGE_REL
    }
    return targets, images


def drawing_ids(element: ET.Element) -> list[str]:
    return [blip.get(R + "embed") for blip in element.findall(".//" + A + "blip") if blip.get(R + "embed")]


def paragraph_markdown(paragraph: ET.Element, targets: dict[str, str], images: dict[str, str], slug: str, count: list[int]) -> str:
    parts = []
    for child in paragraph:
        if child.tag == W + "hyperlink":
            label, url = visible_text(child).strip(), targets.get(child.get(R + "id"))
            parts.append(f"[{label}]({url})" if label and url else label)
            continue
        if child.tag != W + "r":
            continue
        parts.append(visible_text(child))
        for relation_id in drawing_ids(child):
            if relation_id not in images:
                raise ValueError(f"{slug}: image relationship {relation_id!r} is missing")
            count[0] += 1
            extension = Path(images[relation_id]).suffix.lower() or ".bin"
            label = f"{slug.replace('-', ' ').title()} image {count[0]}"
            parts.append(f"\n\n![{label}](posts/assets/{slug}/image-{count[0]}{extension})\n\n")
    value = "".join(parts).strip()
    style = paragraph.find(W + "pPr/" + W + "pStyle")
    name = style.get(W + "val", "") if style is not None else ""
    match = re.fullmatch(r"Heading([1-6])", name)
    return "#" * int(match.group(1)) + " " + value if match and value else value


def convert_docx(docx_path: Path, slug: str, output_posts: Path) -> None:
    with zipfile.ZipFile(docx_path) as document:
        targets, images = relationships(document)
        root = ET.fromstring(document.read("word/document.xml"))
        count = [0]
        markdown = [
            paragraph_markdown(paragraph, targets, images, slug, count)
            for paragraph in root.findall("./" + W + "body/" + W + "p")
        ]
        output_posts.mkdir(parents=True, exist_ok=True)
        (output_posts / f"{slug}.md").write_text(
            "\n\n".join(part for part in markdown if part).strip() + "\n", encoding="utf-8"
        )
        assets = output_posts / "assets" / slug
        assets.mkdir(parents=True, exist_ok=True)
        for index, relation_id in enumerate(drawing_ids(root), 1):
            target = images[relation_id]
            extension = Path(target).suffix.lower() or ".bin"
            with document.open("word/" + target) as source, (assets / f"image-{index}{extension}").open("wb") as destination:
                shutil.copyfileobj(source, destination)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args(argv)
    slugs = {post["slug"] for post in json.loads(args.manifest.read_text(encoding="utf-8"))}
    for document in sorted(args.source.glob("*.docx")):
        if document.stem not in slugs:
            raise SystemExit(f"{document}: no matching slug in {args.manifest}")
        convert_docx(document, document.stem, args.output)


if __name__ == "__main__":
    main()
