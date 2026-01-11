```py
#!/usr/bin/env python3
import argparse
from pathlib import Path
import re


def repo_root() -> Path:
    cur = Path.cwd()
    for parent in [cur] + list(cur.parents):
        if (parent / ".git").exists():
            return parent
    return cur


def read_frontmatter(text: str) -> str:
    parts = text.split("

🌊
