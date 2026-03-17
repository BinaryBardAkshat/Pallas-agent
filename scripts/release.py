#!/usr/bin/env python3
"""
Pallas Release Script
Usage: python scripts/release.py --bump patch|minor|major [--dry-run]

Bumps the version across all relevant files, runs tests, builds the package,
and creates a git tag ready for publishing.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# ─── Paths (relative to repo root) ───────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT  = REPO_ROOT / "pyproject.toml"
AGENT_JSON = REPO_ROOT / "pallas_registry" / "agent.json"
CONSTANTS  = REPO_ROOT / "pallas_core" / "pallas_constants.py"

# ─── ANSI helpers ─────────────────────────────────────────────────────────────
GREEN  = "\033[0;32m"
CYAN   = "\033[0;36m"
YELLOW = "\033[1;33m"
RED    = "\033[0;31m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def ok(msg: str)   -> None: print(f"{GREEN}  [OK]  {msg}{RESET}")
def info(msg: str) -> None: print(f"{CYAN}  -->   {msg}{RESET}")
def warn(msg: str) -> None: print(f"{YELLOW}  [!]   {msg}{RESET}", file=sys.stderr)
def fail(msg: str) -> None:
    print(f"{RED}  [X]   {msg}{RESET}", file=sys.stderr)
    sys.exit(1)
def step(msg: str) -> None: print(f"\n{BOLD}{CYAN}{msg}{RESET}")


# ─── Version helpers ──────────────────────────────────────────────────────────
def parse_version(version_str: str) -> tuple[int, int, int]:
    """Parse 'X.Y.Z' into (major, minor, patch)."""
    m = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version_str.strip())
    if not m:
        fail(f"Cannot parse version string: {version_str!r}")
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def bump_version(current: str, bump: str) -> str:
    """Return new version string after applying bump."""
    major, minor, patch = parse_version(current)
    if bump == "major":
        return f"{major + 1}.0.0"
    elif bump == "minor":
        return f"{major}.{minor + 1}.0"
    elif bump == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        fail(f"Unknown bump type: {bump!r}")


# ─── Version readers ──────────────────────────────────────────────────────────
def read_current_version() -> str:
    """Read version from pyproject.toml."""
    text = PYPROJECT.read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not m:
        fail(f"Could not find version in {PYPROJECT}")
    return m.group(1)


# ─── Version writers ──────────────────────────────────────────────────────────
def update_pyproject(new_version: str, dry_run: bool) -> None:
    text = PYPROJECT.read_text(encoding="utf-8")
    updated = re.sub(
        r'^(version\s*=\s*)"[^"]+"',
        rf'\g<1>"{new_version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if updated == text:
        warn("pyproject.toml: version pattern not matched — no change.")
        return
    if dry_run:
        info(f"[dry-run] Would update {PYPROJECT.relative_to(REPO_ROOT)}")
    else:
        PYPROJECT.write_text(updated, encoding="utf-8")
        ok(f"Updated {PYPROJECT.relative_to(REPO_ROOT)}")


def update_agent_json(new_version: str, dry_run: bool) -> None:
    data = json.loads(AGENT_JSON.read_text(encoding="utf-8"))
    data["version"] = new_version
    if dry_run:
        info(f"[dry-run] Would update {AGENT_JSON.relative_to(REPO_ROOT)}")
    else:
        AGENT_JSON.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        ok(f"Updated {AGENT_JSON.relative_to(REPO_ROOT)}")


def update_constants(new_version: str, dry_run: bool) -> None:
    text = CONSTANTS.read_text(encoding="utf-8")
    updated = re.sub(
        r'^(VERSION\s*=\s*)"[^"]+"',
        rf'\g<1>"{new_version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if updated == text:
        warn("pallas_constants.py: VERSION pattern not matched — no change.")
        return
    if dry_run:
        info(f"[dry-run] Would update {CONSTANTS.relative_to(REPO_ROOT)}")
    else:
        CONSTANTS.write_text(updated, encoding="utf-8")
        ok(f"Updated {CONSTANTS.relative_to(REPO_ROOT)}")


# ─── Shell helpers ────────────────────────────────────────────────────────────
def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> int:
    """Run a subprocess, streaming output, returning exit code."""
    result = subprocess.run(cmd, cwd=cwd or REPO_ROOT)
    if check and result.returncode != 0:
        fail(f"Command failed (exit {result.returncode}): {' '.join(cmd)}")
    return result.returncode


# ─── Main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pallas release helper — bumps version, runs tests, builds, and tags.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/release.py --bump patch
  python scripts/release.py --bump minor --dry-run
  python scripts/release.py --bump major
        """,
    )
    parser.add_argument(
        "--bump",
        choices=["patch", "minor", "major"],
        required=True,
        help="Which semver component to increment.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without making any changes.",
    )
    args = parser.parse_args()

    dry_run: bool = args.dry_run

    # ── Read & compute new version ────────────────────────────────────────────
    step("Reading current version...")
    current_version = read_current_version()
    new_version = bump_version(current_version, args.bump)

    info(f"Current version : {current_version}")
    info(f"Bump type       : {args.bump}")
    info(f"New version     : {new_version}")

    if dry_run:
        print(f"\n{YELLOW}{BOLD}  [DRY-RUN MODE] No files will be modified.{RESET}\n")

    # ── Update version files ──────────────────────────────────────────────────
    step("Updating version in source files...")
    update_pyproject(new_version, dry_run)
    update_agent_json(new_version, dry_run)
    update_constants(new_version, dry_run)

    # ── Run tests ─────────────────────────────────────────────────────────────
    step("Running test suite...")
    if dry_run:
        info("[dry-run] Would run: pytest tests/ -x")
    else:
        run(["pytest", "tests/", "-x", "--tb=short"])
        ok("All tests passed")

    # ── Build package ─────────────────────────────────────────────────────────
    step("Building package...")
    if dry_run:
        info("[dry-run] Would run: uv build")
    else:
        run(["uv", "build"])
        ok("Package built successfully")

    # ── Git tag ───────────────────────────────────────────────────────────────
    step("Creating git tag...")
    tag = f"v{new_version}"
    if dry_run:
        info(f"[dry-run] Would run: git tag {tag}")
    else:
        run(["git", "tag", tag])
        ok(f"Created tag {tag}")

    # ── Done ──────────────────────────────────────────────────────────────────
    print("")
    if dry_run:
        print(f"{YELLOW}{BOLD}  [DRY-RUN] Would release v{new_version} — no changes were made.{RESET}")
    else:
        print(f"{GREEN}{BOLD}  Release v{new_version} ready.{RESET}")
        print(f"{CYAN}  Run: git push && git push --tags{RESET}")
        print(f"{CYAN}  Then: uv publish  (or: twine upload dist/*){RESET}")
    print("")


if __name__ == "__main__":
    main()
