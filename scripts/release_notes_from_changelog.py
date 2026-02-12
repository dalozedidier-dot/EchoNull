from __future__ import annotations

import argparse
import re
from pathlib import Path


def _tag_to_version(tag: str) -> str:
    return tag.lstrip("v").strip()


def extract_section(changelog: str, version: str) -> str:
    # Section headers look like: ## 0.1.2
    pattern = re.compile(rf"(?ms)^##\s+{re.escape(version)}\s*$\n(.*?)(?=^##\s+|\Z)")
    m = pattern.search(changelog)
    if not m:
        raise SystemExit(f"Version {version} not found in CHANGELOG.md")
    body = m.group(1).strip()
    return f"## {version}\n\n{body}\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True, help="Tag name, ex: v0.1.2")
    ap.add_argument("--changelog", default="CHANGELOG.md")
    ap.add_argument("--out", default="release_notes.md")
    args = ap.parse_args()

    version = _tag_to_version(args.tag)
    changelog = Path(args.changelog).read_text(encoding="utf-8")
    section = extract_section(changelog, version)

    Path(args.out).write_text(section, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
