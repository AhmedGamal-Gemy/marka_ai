#!/usr/bin/env uv run python
"""
Auto-generate docs, watch for changes, and serve with live reload.

Usage:
    uv run python scripts/serve_docs.py
    uv run python scripts/serve_docs.py --port 8080

Requirements:
    - watchfiles
    - mkdocstrings-python
    - mkdocs-material
    - zensical
"""

import subprocess
import sys
import threading
import time
import signal
from pathlib import Path
from watchfiles import watch


SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_DIR = SCRIPT_DIR.parent
GENERATOR = SCRIPT_DIR / "generate_api_docs.py"
API_DIR = PROJECT_DIR / "ai" / "app"
DOCS_DIR = PROJECT_DIR / "docs"


class DocsServer:
    """Manages the zensical serve process."""

    def __init__(self, port=8000):
        self.port = port
        self.process = None

    def start(self):
        """Start zensical serve."""
        print(f"[SERVER] Starting zensical serve on port {self.port}...", flush=True)
        self.process = subprocess.Popen(
            [
                "uvx",
                "--with",
                "mkdocstrings-python",
                "--with",
                "mkdocs-material",
                "zensical",
                "serve",
                "-a",
                f"127.0.0.1:{self.port}",
            ],
            cwd=PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(f"[SERVER] Server running at http://127.0.0.1:{self.port}", flush=True)

    def stop(self):
        """Stop zensical serve."""
        if self.process:
            print("[SERVER] Stopping server...", flush=True)
            self.process.terminate()
            self.process.wait()
            print("[SERVER] Server stopped", flush=True)

    def rebuild(self):
        """Rebuild the site."""
        print("[SERVER] Rebuilding site...", flush=True)
        result = subprocess.run(
            [
                "uvx",
                "--with",
                "mkdocstrings-python",
                "--with",
                "mkdocs-material",
                "zensical",
                "build",
            ],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("[SERVER] Site rebuilt", flush=True)
        else:
            print(f"[SERVER] Build failed: {result.stderr}", flush=True)
        return result.returncode == 0


def regenerate_api_docs():
    """Run the API docs generator."""
    print("[WATCH] Regenerating API docs from Python docstrings...", flush=True)
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


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Serve and watch Marka AI docs")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve on")
    args = parser.parse_args()

    server = DocsServer(args.port)
    running = True

    def signal_handler(sig, frame):
        nonlocal running
        print("\n[MAIN] Shutting down...", flush=True)
        running = False
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("=" * 60, flush=True)
    print("  Marka AI Docs Server", flush=True)
    print("  Auto-regenerate + Live Reload", flush=True)
    print("=" * 60, flush=True)
    print(flush=True)

    # Initial build
    print("[MAIN] Initial build...", flush=True)
    regenerate_api_docs()
    server.rebuild()

    # Start server
    server.start()

    print(flush=True)
    print("[MAIN] Watching for changes...", flush=True)
    print("  - Python: ai/app/**/*.py", flush=True)
    print("  - Docs:   docs/**/*.md", flush=True)
    print(flush=True)
    print("  Press Ctrl+C to stop", flush=True)
    print(flush=True)

    # Watch for changes
    try:
        for changes in watch(API_DIR, DOCS_DIR):
            if not running:
                break

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
                server.rebuild()
                print("[WATCH] Watching for changes...", flush=True)

    except Exception as e:
        print(f"[MAIN] Error: {e}", flush=True)
    finally:
        server.stop()


if __name__ == "__main__":
    main()
