#!/usr/bin/env uv run python
"""
Watch Python and markdown files, auto-regenerate docs and rebuild site.

Usage:
    uv run python scripts/watch_docs.py

Requirements:
    - watchfiles
    - mkdocstrings-python
    - mkdocs-material
"""

import subprocess
import sys
from pathlib import Path
from watchfiles import watch


SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
GENERATOR = SCRIPT_DIR / "generate_api_docs.py"
API_DIR = PROJECT_DIR / "ai" / "app"
DOCS_DIR = PROJECT_DIR / "docs"


def regenerate_api_docs():
    """Run the API docs generator."""
    print("[WATCH] Detected .py changes, regenerating API docs...", flush=True)
    result = subprocess.run(
        ["uv", "run", str(GENERATOR)],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
    )
    if result.returncode == 0:
        print("[WATCH] API docs regenerated successfully", flush=True)
    else:
        print(f"[WATCH] Warning: Generator failed: {result.stderr}", flush=True)
    return result.returncode == 0


def rebuild_site():
    """Trigger zensical rebuild."""
    print("[WATCH] Rebuilding site...", flush=True)


def main():
    print("=" * 60, flush=True)
    print("  Marka AI Docs Watcher", flush=True)
    print("  Auto-regenerates API docs from Python docstrings", flush=True)
    print("=" * 60, flush=True)
    print(flush=True)
    print("[WATCH] Watching for changes...", flush=True)
    print("  - Python: ai/app/**/*.py", flush=True)
    print("  - Docs:   docs/**/*.md", flush=True)
    print(flush=True)
    print("  Press Ctrl+C to stop", flush=True)
    print(flush=True)

    try:
        for changes in watch(API_DIR, DOCS_DIR):
            py_changes = [c for c in changes if c[1].endswith(".py")]
            md_changes = [c for c in changes if c[1].endswith(".md")]

            if py_changes:
                print("\n[WATCH] Python files changed:", flush=True)
                for change_type, path in py_changes:
                    change_str = (
                        "added"
                        if change_type == 1
                        else "modified"
                        if change_type == 2
                        else "removed"
                    )
                    print(
                        f"  - [{change_str}] {Path(path).relative_to(PROJECT_DIR)}",
                        flush=True,
                    )
                regenerate_api_docs()

            if md_changes:
                print("\n[WATCH] Markdown files changed:", flush=True)
                for change_type, path in md_changes:
                    change_str = (
                        "added"
                        if change_type == 1
                        else "modified"
                        if change_type == 2
                        else "removed"
                    )
                    print(
                        f"  - [{change_str}] {Path(path).relative_to(PROJECT_DIR)}",
                        flush=True,
                    )

            if py_changes or md_changes:
                rebuild_site()
                print("[WATCH] Watching for changes...", flush=True)

    except KeyboardInterrupt:
        print("\n[WATCH] Stopped", flush=True)
        sys.exit(0)


if __name__ == "__main__":
    main()
