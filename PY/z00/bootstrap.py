#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path


def repo_root() -> Path:
    cur = Path.cwd()
    for parent in [cur] + list(cur.parents):
        if (parent / ".git").exists():
            return parent
    return cur


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("

🌊
