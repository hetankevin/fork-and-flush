#!/usr/bin/env python3
"""Install the bundled skill without modifying app configuration. Python 3.9+."""
import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil
import sys
import tempfile

NAME = "fork-and-flush"
SOURCE = Path(__file__).resolve().parents[1] / "skills" / NAME


def digest(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob("*") if p.is_file()
            and "__pycache__" not in p.parts and p.suffix != ".pyc"}


def install(source, root, replace=False):
    destination = root.expanduser() / NAME
    if not (source / "SKILL.md").is_file():
        raise ValueError("source does not contain SKILL.md")
    if destination.is_symlink():
        raise ValueError(f"refusing to replace symlink: {destination}")
    if destination.exists():
        if destination.is_dir() and digest(source) == digest(destination):
            return f"Already current: {destination}"
        if not replace:
            raise ValueError(f"destination exists: {destination}; use --replace to back it up")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".fork-and-flush-", dir=destination.parent) as tmp:
        staged = Path(tmp) / NAME
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if digest(source) != digest(staged):
            raise ValueError("staged copy verification failed")
        backup = None
        if destination.exists():
            # Backups live outside skill discovery roots to avoid duplicate skills.
            backup_root = destination.parent.parent / "skill-backups"
            backup_root.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            backup = backup_root / f"{NAME}-{stamp}"
            destination.rename(backup)
        try:
            staged.rename(destination)
        except OSError:
            if backup is not None:
                backup.rename(destination)
            raise
    return f"Installed: {destination}" + (f" (backup: {backup})" if backup else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("codex", "claude", "both"), default="both")
    parser.add_argument("--codex-dir", type=Path, default=Path.home() / ".agents/skills",
                        help="Codex skill root; older installations may use ~/.codex/skills")
    parser.add_argument("--claude-dir", type=Path, default=Path.home() / ".claude/skills")
    parser.add_argument("--replace", action="store_true", help="back up a different existing installation")
    args = parser.parse_args()
    roots = []
    if args.target in ("codex", "both"):
        roots.append(args.codex_dir)
    if args.target in ("claude", "both"):
        roots.append(args.claude_dir)
    try:
        for root in dict.fromkeys(roots):
            print(install(SOURCE, root, args.replace))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
