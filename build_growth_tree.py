#!/usr/bin/env python3
"""Build growth-path JSON and attachment files from a folder tree.

Example:
  python build_growth_tree.py "E:\\W.O.R.K\\成长地图\\0623"
  python build_growth_tree.py

Output by default:
  ./data.json
  ./attachments/
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
from pathlib import Path

from PIL import Image, UnidentifiedImageError


IMAGE_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg", ".gif", ".bmp"}
TEXT_EXTENSIONS = {".txt", ".md"}
DEFAULT_OUTPUT_JSON = "data.json"
DEFAULT_ATTACHMENTS_DIR = "attachments"
DEFAULT_SOURCE_DIR = r"E:\W.O.R.K\成长地图\0623"
DEFAULT_OUTPUT_DIR = "output"
ROOT_GROUP_NAMES = {"相关专业", "非相关专业"}


def natural_key(value: Path) -> list[object]:
    parts = re.split(r"(\d+)", value.name)
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def safe_filename(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\s]+', "", value)
    return cleaned or "attachment"


def clean_cli_value(value: str) -> str:
    return value.strip().strip('"').strip("'").strip("\ufeff").strip()


def parse_year(name: str) -> int | None:
    patterns = [
        r"第\s*(\d+)\s*年",
        r"(\d+)\s*年",
        r"year\s*(\d+)",
        r"y\s*(\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def is_root_group_directory(path: Path) -> bool:
    return path.name in ROOT_GROUP_NAMES


def display_name(path: Path) -> str:
    name = path.stem if path.is_file() else path.name
    name = re.sub(r"^第\s*\d+\s*年[:：\-_\s]*", "", name)
    name = re.sub(r"^\d+\s*年[:：\-_\s]*", "", name)
    return name


def first_file(files: list[Path], extensions: set[str]) -> Path | None:
    matched = [item for item in files if item.suffix.lower() in extensions]
    return sorted(matched, key=natural_key)[0] if matched else None


def find_matching_image(text_file: Path, files: list[Path]) -> Path | None:
    text_stem = text_file.stem
    display = display_name(text_file)
    images = [item for item in files if item.suffix.lower() in IMAGE_EXTENSIONS]

    for image in images:
        if image.stem == text_stem:
            return image

    for image in images:
        if display and display in image.stem:
            return image

    return None


def read_text(source: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return source.read_text(encoding=encoding).strip()
        except UnicodeDecodeError:
            continue

    return source.read_text(errors="ignore").strip()


def read_text_base64(source: Path) -> str:
    text = read_text(source)
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def find_matching_supplement_dir(text_file: Path, directories: list[Path]) -> Path | None:
    text_stem = text_file.stem
    display = display_name(text_file)

    for directory in directories:
        if directory.name == text_stem:
            return directory

    for directory in directories:
        if display and display in directory.name:
            return directory

    return None


def collect_files(directory: Path, ignored_paths: set[Path]) -> list[Path]:
    files = []
    for item in directory.rglob("*"):
        if item.is_file() and not is_ignored(item, ignored_paths):
            files.append(item)
    return sorted(files, key=natural_key)


def find_pic_detail_file(files: list[Path]) -> Path | None:
    for item in files:
        if item.suffix.lower() in TEXT_EXTENSIONS and item.stem == "资料":
            return item

    return None


def copy_attachment(source: Path, attachments_dir: Path, prefix_parts: list[str]) -> str | None:
    suffix = ".webp" if source.suffix.lower() in IMAGE_EXTENSIONS else source.suffix.lower()
    target_name = f"{safe_filename(''.join(prefix_parts))}{suffix}"
    target = attachments_dir / target_name
    counter = 2

    while target.exists():
        target_name = f"{safe_filename(''.join(prefix_parts))}_{counter}{suffix}"
        target = attachments_dir / target_name
        counter += 1

    if source.suffix.lower() in IMAGE_EXTENSIONS:
        if not convert_image_to_webp(source, target):
            return None
    else:
        shutil.copy2(source, target)

    return f"./{attachments_dir.name}/{target.name}"


def convert_image_to_webp(source: Path, target: Path) -> bool:
    if source.suffix.lower() == ".webp":
        shutil.copy2(source, target)
        return True

    try:
        with Image.open(source) as image:
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
            image.save(target, "WEBP", quality=88, method=6)
            return True
    except (UnidentifiedImageError, OSError) as exc:
        print(f"Warning: skip invalid image {source} ({exc})")
        return False


def make_detail_node(path: Path, files: list[Path], attachments_dir: Path, ancestors: list[str]) -> dict:
    node_name = display_name(path)
    node: dict[str, object] = {
        "name": node_name,
        "detail": True,
    }

    year = parse_year(path.name)
    if year is not None:
        node["year"] = year

    image = first_file(files, IMAGE_EXTENSIONS)
    text = first_file(files, TEXT_EXTENSIONS)
    prefix_parts = ancestors + [node_name]

    if image:
        pic = copy_attachment(image, attachments_dir, prefix_parts)
        if pic:
            node["pic"] = pic
            pic_detail = find_pic_detail_file(files)
            if pic_detail:
                node["picDetail"] = read_text_base64(pic_detail)

    if text:
        node["txt"] = read_text_base64(text)

    return node


def make_text_file_node(
    text_file: Path,
    files: list[Path],
    attachments_dir: Path,
    ancestors: list[str],
    supplement_dir: Path | None = None,
    ignored_paths: set[Path] | None = None,
) -> dict:
    node_name = display_name(text_file)
    node: dict[str, object] = {
        "name": node_name,
        "detail": False,
    }

    year = parse_year(text_file.stem)
    if year is not None:
        node["year"] = year

    supplement_files = []
    if supplement_dir and ignored_paths is not None:
        supplement_files = collect_files(supplement_dir, ignored_paths)

    all_related_files = files + supplement_files
    prefix_parts = ancestors + [node_name]
    image = find_matching_image(text_file, files) or first_file(supplement_files, IMAGE_EXTENSIONS)

    node["txt"] = read_text_base64(text_file)
    if image:
        pic = copy_attachment(image, attachments_dir, prefix_parts)
        if pic:
            node["pic"] = pic
            node["detail"] = True
            pic_detail = find_pic_detail_file(supplement_files)
            if pic_detail:
                node["picDetail"] = read_text_base64(pic_detail)

    return node


def is_ignored(path: Path, ignored_paths: set[Path]) -> bool:
    resolved = path.resolve()
    return resolved in ignored_paths or any(parent in ignored_paths for parent in resolved.parents)


def build_node(
    path: Path,
    attachments_dir: Path,
    ancestors: list[str],
    ignored_paths: set[Path],
    depth: int = 0,
    force_root: bool = False,
) -> dict | None:
    directories = sorted(
        [item for item in path.iterdir() if item.is_dir() and not is_ignored(item, ignored_paths)],
        key=natural_key,
    )
    files = sorted(
        [item for item in path.iterdir() if item.is_file() and not is_ignored(item, ignored_paths)],
        key=natural_key,
    )
    text_files = sorted([item for item in files if is_text_file(item)], key=natural_key)
    supplement_dirs = {
        text_file: find_matching_supplement_dir(text_file, directories)
        for text_file in text_files
    }
    used_supplement_dirs = {directory for directory in supplement_dirs.values() if directory is not None}
    directories = [directory for directory in directories if directory not in used_supplement_dirs]
    paired_images = {
        image
        for text_file in text_files
        for related_files in [
            files + (collect_files(supplement_dirs[text_file], ignored_paths) if supplement_dirs[text_file] else [])
        ]
        for image in [find_matching_image(text_file, related_files)]
        if image is not None
    }
    non_detail_files = [item for item in files if item not in text_files]
    useful_files = [
        item
        for item in non_detail_files
        if item not in paired_images and (item.suffix.lower() in IMAGE_EXTENSIONS or item.suffix.lower() in TEXT_EXTENSIONS)
    ]

    has_only_root_group_children = (
        depth == 1
        and directories
        and all(is_root_group_directory(directory) for directory in directories)
    )

    node: dict[str, object] = {"name": path.name}
    if force_root or (depth == 1 and not has_only_root_group_children):
        node["root"] = True

    children = []
    child_force_root = has_only_root_group_children
    for directory in directories:
        child = build_node(
            directory,
            attachments_dir,
            ancestors + [path.name],
            ignored_paths,
            depth + 1,
            child_force_root,
        )
        if child:
            children.append(child)

    for text_file in text_files:
        children.append(
            make_text_file_node(
                text_file,
                files,
                attachments_dir,
                ancestors + [path.name],
                supplement_dirs[text_file],
                ignored_paths,
            )
        )

    if useful_files:
        if directories or children:
            children.append(make_detail_node(path, useful_files, attachments_dir, ancestors + [path.name]))
        else:
            detail_node = make_detail_node(path, useful_files, attachments_dir, ancestors)
            if force_root or (depth == 1 and not has_only_root_group_children):
                detail_node["root"] = True
            return detail_node

    if children:
        node["children"] = children
        return node

    return None


def build_tree(source_dir: Path, attachments_dir: Path, output_json: Path) -> list[dict]:
    ignored_paths = {attachments_dir.resolve(), output_json.resolve()}
    roots = []
    for directory in sorted(
        [item for item in source_dir.iterdir() if item.is_dir() and not is_ignored(item, ignored_paths)],
        key=natural_key,
    ):
        node = build_node(directory, attachments_dir, [], ignored_paths, 0)
        if node:
            roots.append(node)

    return roots


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate growth-path data.json and attachments from a folder tree.")
    parser.add_argument("source", nargs="?", help="Source directory, for example E:\\W.O.R.K\\成长地图\\0623")
    parser.add_argument("-o", "--output", default=None, help="Output JSON file path.")
    parser.add_argument(
        "-a",
        "--attachments",
        default=None,
        help="Attachment output directory.",
    )
    parser.add_argument("--clean", action="store_true", help="Clean output JSON and attachment directory before generating.")
    args = parser.parse_args()

    source = args.source
    if not source:
        prompt = f"请输入要遍历的源目录，直接回车使用默认目录 [{DEFAULT_SOURCE_DIR}]："
        source = clean_cli_value(input(prompt)) or DEFAULT_SOURCE_DIR
    else:
        source = clean_cli_value(source)

    output_dir = Path(DEFAULT_OUTPUT_DIR)
    source_dir = Path(source).resolve()
    output_json = Path(args.output or output_dir / DEFAULT_OUTPUT_JSON).resolve()
    attachments_dir = Path(args.attachments or output_dir / DEFAULT_ATTACHMENTS_DIR).resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        raise SystemExit(f"Source directory does not exist: {source_dir}")

    if args.clean:
        if output_json.exists():
            output_json.unlink()
        if attachments_dir.exists():
            shutil.rmtree(attachments_dir)

    attachments_dir.mkdir(parents=True, exist_ok=True)
    data = build_tree(source_dir, attachments_dir, output_json)

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Generated {output_json}")
    print(f"Copied attachments to {attachments_dir}")
    print(f"Root items: {len(data)}")


if __name__ == "__main__":
    main()
