#!/usr/bin/env python3
"""Generate the article list in docs/index.md from the Markdown files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
INDEX_PATH = DOCS_DIR / "index.md"

START_MARKER = "<!-- auto-index:start -->"
END_MARKER = "<!-- auto-index:end -->"

CATEGORY_TITLES = {
    "os": "OS",
    "network": "ネットワーク",
    "devices": "デバイス",
    "virtualization": "VM/コンテナ/互換レイヤ",
    "package-manager": "パッケージマネージャ",
    "desktop-linux": "デスクトップ全般 (Linux)",
    "desktop-windows": "デスクトップ全般 (Windows)",
    "apps": "デスクトップアプリ",
    "ui": "UI",
    "development": "開発",
}

HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"^- \[[^]]+\]\(([^)]+)\)$", re.MULTILINE)


def article_title(path: Path) -> str | None:
    """Return the first level-one heading, or None for an unfinished article."""
    match = HEADING_RE.search(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def existing_order(index: str) -> dict[str, int]:
    """Keep the hand-curated article order already present in the index."""
    return {
        link.removeprefix("./"): position
        for position, link in enumerate(LINK_RE.findall(index))
    }


def generated_index(index: str) -> str:
    order = existing_order(index)
    category_rank = {name: rank for rank, name in enumerate(CATEGORY_TITLES)}
    articles: dict[str, list[tuple[str, str]]] = {}

    for path in sorted((DOCS_DIR / "tech").glob("*/*.md")):
        title = article_title(path)
        if title is None:
            continue
        relative = path.relative_to(DOCS_DIR).as_posix()
        articles.setdefault(path.parent.name, []).append((relative, title))

    categories = sorted(
        articles,
        key=lambda name: (category_rank.get(name, len(category_rank)), name),
    )

    lines = [START_MARKER, "## 技術"]
    for category in categories:
        lines.append(f"### {CATEGORY_TITLES.get(category, category)}")
        items = sorted(
            articles[category],
            key=lambda item: (order.get(item[0], len(order)), item[0]),
        )
        lines.extend(f"- [{title}](./{relative})" for relative, title in items)
    lines.append(END_MARKER)
    return "\n".join(lines)


def update_index(*, check: bool = False) -> bool:
    current = INDEX_PATH.read_text(encoding="utf-8")
    generated = generated_index(current)

    if START_MARKER in current and END_MARKER in current:
        before, remainder = current.split(START_MARKER, 1)
        _, after = remainder.split(END_MARKER, 1)
        updated = before.rstrip() + "\n\n" + generated + after
    else:
        # Migrate the current index: its article list starts at this heading.
        before, separator, _ = current.partition("## 技術")
        if not separator:
            raise RuntimeError(f"{INDEX_PATH} has no generated-index markers or '## 技術' heading")
        updated = before.rstrip() + "\n\n" + generated + "\n"

    if updated == current:
        return False
    if check:
        return True

    INDEX_PATH.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit with status 1 instead of updating an out-of-date index",
    )
    args = parser.parse_args()

    changed = update_index(check=args.check)
    if args.check and changed:
        print(f"{INDEX_PATH.relative_to(ROOT)} is out of date; run scripts/update_index.py")
        return 1
    if changed:
        print(f"updated {INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
