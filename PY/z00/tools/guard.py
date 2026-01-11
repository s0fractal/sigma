#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path


def repo_root() -> Path:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL
        ).decode("utf-8", errors="ignore").strip()
        if out:
            return Path(out)
    except Exception:
        pass
    return Path.cwd()


def log_err(msg, errors):
    print(f"❌ RULE BROKEN: {msg}")
    errors.append(msg)


def log_fix(msg):
    print(f"   🛠  FIXING: {msg}")


def find_root_code(root: Path):
    return [
        p for p in root.iterdir()
        if p.is_file() and p.suffix in {".ts", ".rs", ".js"}
    ]


def find_shadow_readmes(root: Path):
    paths = []
    for dim in ("ts", "rs", "lean"):
        dim_dir = root / dim
        if not dim_dir.exists():
            continue
        paths.extend(dim_dir.rglob("README.md"))
    return paths


def find_noncanonical_keys(root: Path):
    bad = []
    key_re = re.compile(r"^\s*(dna|DNA|spectrum|SPECTRUM|physics|PHYSICS|"
                        r"energy|ENERGY|mass|MASS|entropy|ENTROPY|"
                        r"complexity|COMPLEXITY):")
    for path in root.glob("sigma/**/*.sigma"):
        try:
            for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if key_re.match(line):
                    bad.append(f"{path}:{i}:{line}")
        except Exception:
            continue
    return bad


def spectrum_missing_glyph(root: Path):
    missing = []
    for path in (root / "sigma" / "spectrum").glob("*.sigma"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        if not re.search(r"^\s*GLYPH:", text, re.MULTILINE):
            missing.append(str(path))
    return missing


def fix_sigma_keys(root: Path):
    for path in root.glob("sigma/**/*.sigma"):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        new = text
        new = new.replace("\nSPECTRUM:", "\n🌈SPECTRUM:")
        new = new.replace("\nspectrum:", "\n🌈SPECTRUM:")
        new = new.replace("\nPHYSICS:", "\n⚖️PHYSICS:
  ENTROPY: -1
        new = new.replace("\nphysics:", "\n⚖️PHYSICS:
  ENTROPY: -1
        new = new.replace("\nENERGY:", "\n⚡ENERGY:")
        new = new.replace("\nenergy:", "\n⚡ENERGY:")
        new = new.replace("\ndna:", "\n🧬DNA:")
        new = new.replace("\nDNA:", "\n🧬DNA:")
        new = new.replace("\nmass:", "\n🪨MASS:")
        new = new.replace("\n  mass:", "\n  🪨MASS:")
        new = new.replace("\nentropy:", "\n🌀ENTROPY:")
        new = new.replace("\n  entropy:", "\n  🌀ENTROPY:")
        new = new.replace("\ncomplexity:", "\n🧩COMPLEXITY:")
        new = new.replace("\n  complexity:", "\n  🧩COMPLEXITY:")
        # Remove standalone 🌈 marker lines
        lines = [ln for ln in new.splitlines() if ln.strip() != "🌈"]
        new = "\n".join(lines)
        if text.endswith("\n"):
            new += "\n"
        if new != text:
            path.write_text(new, encoding="utf-8")


def missing_dna(root: Path):
    missing = []
    for level in range(0, 9):
        for path in (root / "sigma" / str(level)).glob("*.sigma"):
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            if not re.search(r"^\s*🧬DNA:", text, re.MULTILINE):
                missing.append(str(path))
    return missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()

    root = repo_root()
    errors = []

    print("🛡️  Guarding the Void...")

    # RULE 1: NO CODE IN VOID ROOT
    stray = find_root_code(root)
    if stray:
        log_err("Code found in Void Root (Must be in nodes/)", errors)
        for p in stray:
            print(p)
        if args.fix:
            target = root / "intents" / "drafts"
            target.mkdir(parents=True, exist_ok=True)
            for p in stray:
                shutil.move(str(p), str(target / p.name))
            log_fix("Moved stray code to intents/drafts/")

    # RULE 2: NODES MUST BE SUBMODULES
    nodes_dir = root / "nodes"
    if nodes_dir.exists():
        for node in nodes_dir.iterdir():
            if node.is_dir() and not (node / ".git").exists():
                log_err(f"Node {node.name} is a raw folder, not a submodule!", errors)

    # RULE 3: NO README IN CODE DIMENSIONS
    shadow = find_shadow_readmes(root)
    if shadow:
        log_err("Shadow READMEs found in code dimensions (Noise detected)", errors)
        for p in shadow:
            print(p)
        if args.fix:
            for p in shadow:
                p.unlink(missing_ok=True)
            log_fix("Purged shadow READMEs.")

    # RULE 4: SIGMA FRONTMATTER CANON (GLYPH+UPPERCASE KEYS)
    bad = find_noncanonical_keys(root)
    if bad:
        log_err("Non-canonical sigma keys detected (use 🧬DNA, ⚡ENERGY, 🌈SPECTRUM, ⚖️PHYSICS)", errors)
        for line in bad:
            print(line)
        if args.fix:
            log_fix("Rewriting sigma keys to GLYPH+UPPERCASE")
            fix_sigma_keys(root)

    missing = missing_dna(root)
    if missing:
        log_err("Missing 🧬DNA in sigma frontmatter", errors)
        for path in missing:
            print(path)

    spectrum_missing = spectrum_missing_glyph(root)
    if spectrum_missing:
        log_err("Spectrum frontmatter missing GLYPH", errors)
        for path in spectrum_missing:
            print(path)

    if not errors:
        print("✅ Structure is Sacred.")
        return 0
    print(f"⚠️  Found {len(errors)} violations.")
    if not args.fix:
        print("   Run with --fix to attempt auto-repair.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
