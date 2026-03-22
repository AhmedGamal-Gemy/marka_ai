#!/usr/bin/env python
"""
Auto-generate API reference docs from Python source code.

Scans ai/app/ directory and creates markdown docs with proper hierarchy:
  - Packages (dirs with __init__.py)  ->  <n>/index.md   (::: app.<n>)
  - Standalone .py files              ->  <n>.md          (::: app.<path>.<n>)
  - Nested packages                   ->  <a>/<b>/index.md   (::: app.<a>.<b>)

Also updates the `nav:` section of mkdocs.yml automatically.

Usage:
    python generate_api_docs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SRC_DIR   = Path("ai/app")
DOCS_DIR  = Path("docs/reference/api")
DOCS_BASE = Path("docs")          # root of the mkdocs docs/ folder
MKDOCS    = Path("mkdocs.yml")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_docstring(py_file: Path) -> str:
    """
    Return the module-level docstring from a .py file, or \'\'.

    Uses ast.get_docstring() so only the very first expression of the *module*
    is considered.  Function/class/method docstrings that appear earlier in the
    raw text are never accidentally returned.
    """
    import ast

    try:
        src = py_file.read_text(encoding="utf-8")
        tree = ast.parse(src, filename=str(py_file))
        return ast.get_docstring(tree) or ""
    except (OSError, SyntaxError):
        return ""


def make_title(stem: str) -> str:
    """
    Prettify a snake_case filename stem into a nav/page title.

    Known technical acronyms are always uppercased regardless of position.
    Examples:
        "api"        -> "API"
        "llm"        -> "LLM"
        "test_llm"   -> "Test LLM"
        "api_v1"     -> "API V1"
        "rag"        -> "RAG"
    """
    # Acronyms that should always be fully uppercased
    ACRONYMS = {
        "api", "llm", "rag", "orm", "sql", "db", "ai", "ml",
        "nlp", "cli", "sdk", "jwt", "mcp", "url", "http",
        "rest", "grpc", "json", "yaml", "id", "ids",
        "v1", "v2", "v3", "v4",
    }
    words = stem.replace("_", " ").replace("-", " ").split()
    result = []
    for i, word in enumerate(words):
        lower = word.lower()
        if lower in ACRONYMS:
            result.append(lower.upper())
        elif i == 0:
            result.append(word.capitalize())
        else:
            result.append(word.capitalize())
    return " ".join(result)


def rel_to_module(rel: Path) -> str:
    """
    Convert a path relative to SRC_DIR (without extension) to a dotted module name.

    Examples
    --------
    Path(".")                     ->  "app"
    Path("agents")                ->  "app.agents"
    Path("api/v1/middleware")     ->  "app.api.v1.middleware"
    Path("services/test_service") ->  "app.services.test_service"
    """
    if rel == Path("."):
        return "app"
    return "app." + ".".join(rel.parts)


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover(src: Path) -> tuple[list[Path], list[Path]]:
    """
    Walk *src* and return (packages, standalone_modules).

    packages           - directories that contain __init__.py (including src itself)
    standalone_modules - .py files that are NOT __init__.py
    """
    packages:   list[Path] = []
    standalone: list[Path] = []

    if (src / "__init__.py").exists():
        packages.append(src)

    for path in sorted(src.rglob("*")):
        if path.is_dir():
            if (path / "__init__.py").exists():
                packages.append(path)
        elif path.is_file() and path.suffix == ".py" and path.name != "__init__.py":
            standalone.append(path)

    return packages, standalone


# ---------------------------------------------------------------------------
# Doc generation
# ---------------------------------------------------------------------------

def write_doc(out_path: Path, title: str, module: str, description: str = "") -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"# {title}\n\n::: {module}\n", encoding="utf-8")


def generate_package_doc(pkg_dir: Path) -> tuple[Path, str]:
    """
    Generate index.md for a package.

      ai/app/         ->  docs/reference/api/app/index.md   (::: app)
      ai/app/api/     ->  docs/reference/api/api/index.md   (::: app.api)
      ai/app/api/v1/  ->  docs/reference/api/api/v1/index.md

    Returns (out_path, module_name).
    """
    init_py = pkg_dir / "__init__.py"

    if pkg_dir == SRC_DIR:
        rel_dir = Path("app")
        module  = "app"
    else:
        rel_dir = pkg_dir.relative_to(SRC_DIR)
        module  = rel_to_module(rel_dir)

    title    = make_title(rel_dir.name)
    desc     = get_docstring(init_py)
    out_path = DOCS_DIR / rel_dir / "index.md"
    write_doc(out_path, title, module, desc)
    return out_path, module


def generate_module_doc(py_file: Path) -> tuple[Path, str]:
    """
    Generate <stem>.md for a standalone module.

      ai/app/main.py                  ->  docs/reference/api/main.md
      ai/app/services/test_service.py ->  docs/reference/api/services/test_service.md

    Returns (out_path, module_name).
    """
    rel_file   = py_file.relative_to(SRC_DIR)
    rel_no_ext = rel_file.with_suffix("")
    module     = rel_to_module(rel_no_ext)
    title      = make_title(py_file.stem)
    desc       = get_docstring(py_file)
    out_path   = DOCS_DIR / rel_no_ext.with_suffix(".md")
    write_doc(out_path, title, module, desc)
    return out_path, module


def generate_index(all_docs: list[Path]) -> Path:
    """Write the top-level docs/reference/api/index.md."""
    lines: list[str] = [
        "# API Reference",
        "",
        "> Auto-generated from `ai/app/` — do not edit manually.",
        "",
        "## Modules",
        "",
    ]

    for doc in sorted(all_docs):
        rel   = doc.relative_to(DOCS_DIR)
        depth = len(rel.parts) - 1
        label = (rel.parts[-2] if len(rel.parts) > 1 else "app") if rel.stem == "index" else rel.stem
        label  = label.replace("_", " ").title()
        indent = "  " * depth
        link   = str(rel).replace("\\", "/")
        lines.append(f"{indent}- [{label}]({link})")

    lines += [
        "",
        "---",
        "",
        "## How It Works",
        "",
        "- **Source**: `ai/app/` directory",
        "- **Format**: Google-style docstrings",
        "- **Generator**: `generate_api_docs.py` — runs automatically on build",
    ]

    out = DOCS_DIR / "index.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# mkdocs.yml nav update
# ---------------------------------------------------------------------------

def _build_tree(doc_paths: list[Path]) -> dict:
    """
    Build a nested dict from the list of generated doc paths.

    Tree keys   - path parts relative to DOCS_DIR  (e.g. agents/index.md)
    Leaf values - mkdocs-relative path strings      (e.g. reference/api/agents/index.md)

    Using DOCS_DIR for keys means the tree directly mirrors the output
    directory with no spurious wrapper levels.
    """
    tree: dict[str, Any] = {}
    for doc in sorted(doc_paths):
        key_rel = doc.relative_to(DOCS_DIR)
        val_str = str(doc.relative_to(DOCS_BASE)).replace("\\", "/")
        parts   = key_rel.parts
        node    = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = val_str
    return tree


def _tree_to_nav(tree: dict) -> list | str:
    """
    Recursively convert the path tree to a mkdocs nav list.

    A directory with ONLY index.md collapses to a bare path string (the
    caller wraps it with a label).  A directory with children becomes a
    list starting with an "Overview" entry.
    """
    index_path = tree.get("index.md")
    children   = {k: v for k, v in tree.items() if k != "index.md"}

    if not children:
        return index_path or []  # type: ignore[return-value]

    nav: list = []
    if index_path:
        nav.append({"Overview": index_path})

    for key in sorted(children):
        value = children[key]
        label = make_title(key.removesuffix(".md"))
        sub   = _tree_to_nav(value) if isinstance(value, dict) else value
        nav.append({label: sub})

    return nav


def _serialize_nav(nav: list | str, indent: int = 0) -> str:
    """Serialize a mkdocs nav structure to an indented YAML string."""
    pad   = "  " * indent
    lines: list[str] = []

    if isinstance(nav, str):
        return nav  # bare path — caller supplies the label

    for item in nav:
        if isinstance(item, str):
            lines.append(f"{pad}- {item}")
        elif isinstance(item, dict):
            for label, value in item.items():
                if isinstance(value, str):
                    lines.append(f"{pad}- {label}: {value}")
                else:
                    lines.append(f"{pad}- {label}:")
                    lines.append(_serialize_nav(value, indent + 1))

    return "\n".join(lines)


def _print_nav_hint(all_docs: list[Path]) -> None:
    """Print the nav YAML to stdout for manual insertion."""
    tree     = _build_tree(all_docs)
    nav_yaml = _serialize_nav(_tree_to_nav(tree), indent=0)
    print("\n[HINT] Add this to your mkdocs.yml nav section:\n")
    print("  - API Reference:")
    for line in nav_yaml.splitlines():
        print(f"    {line}")
    print()


def update_mkdocs_nav(all_docs_including_index: list[Path]) -> None:
    """
    Rewrite (or insert) the 'API Reference' section inside mkdocs.yml nav.

    Uses a line-by-line approach so every other part of the file —
    including comments and unrelated sections — is preserved exactly.
    """
    if not MKDOCS.exists():
        print(f"[WARN] {MKDOCS} not found — skipping nav update")
        _print_nav_hint(all_docs_including_index)
        return

    tree        = _build_tree(all_docs_including_index)
    nav_content = _tree_to_nav(tree)
    nav_yaml    = _serialize_nav(nav_content, indent=0)

    lines = MKDOCS.read_text(encoding="utf-8").splitlines(keepends=True)

    # ---- Locate existing "- API Reference:" and its indentation ----------
    api_ref_idx    : int | None = None
    api_ref_indent : int        = 2

    for i, raw_line in enumerate(lines):
        stripped = raw_line.lstrip()
        if re.match(r"- API Reference\s*:", stripped):
            api_ref_idx    = i
            api_ref_indent = len(raw_line) - len(stripped)
            break

    # ---- Build replacement block with matching indentation ---------------
    pad       = " " * api_ref_indent
    new_block : list[str] = [f"{pad}- API Reference:\n"]
    for nav_line in nav_yaml.splitlines():
        new_block.append(f"{pad}  {nav_line}\n" if nav_line else "\n")

    # ---- Splice into the file --------------------------------------------
    if api_ref_idx is not None:
        # Find where the old block ends: the next sibling nav item at the
        # same indent level, or any line at a lesser indent.
        end = api_ref_idx + 1
        while end < len(lines):
            raw = lines[end]
            if not raw.strip():
                end += 1
                continue
            cur_indent  = len(raw) - len(raw.lstrip())
            is_nav_item = raw.lstrip().startswith("- ")
            if cur_indent <= api_ref_indent and is_nav_item:
                break          # sibling nav item
            if cur_indent < api_ref_indent:
                break          # left the nav section entirely
            end += 1

        new_lines = lines[:api_ref_idx] + new_block + lines[end:]

    else:
        # No existing block — append at the tail of the nav: section.
        nav_idx: int | None = None
        for i, raw_line in enumerate(lines):
            if re.match(r"nav\s*:", raw_line):
                nav_idx = i
                break

        if nav_idx is not None:
            insert_at = nav_idx + 1
            while insert_at < len(lines):
                raw = lines[insert_at]
                if raw.strip() and not raw[0].isspace():
                    break      # hit a new top-level YAML key
                insert_at += 1
            new_lines = lines[:insert_at] + new_block + lines[insert_at:]
        else:
            new_lines = lines + ["\nnav:\n"] + new_block

    MKDOCS.write_text("".join(new_lines), encoding="utf-8")
    print(f"  [+] {MKDOCS}  (nav updated)")


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

def clean_docs_dir() -> None:
    """Remove all previously generated files inside DOCS_DIR."""
    if not DOCS_DIR.exists():
        DOCS_DIR.mkdir(parents=True)
        return

    for path in sorted(DOCS_DIR.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass

    DOCS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not SRC_DIR.exists():
        print(f"[ERROR] Source directory not found: {SRC_DIR}", file=sys.stderr)
        sys.exit(1)

    print(f"[SCAN] Scanning {SRC_DIR}/ for modules...")

    clean_docs_dir()
    print("[CLEAN] Removed old docs\n")

    packages, standalone = discover(SRC_DIR)
    all_docs: list[Path] = []

    # Packages
    for pkg_dir in packages:
        out, module = generate_package_doc(pkg_dir)
        print(f"  [pkg] {out.relative_to(DOCS_DIR)}  ->  ::: {module}")
        all_docs.append(out)

    # Standalone modules
    for py_file in standalone:
        out, module = generate_module_doc(py_file)
        print(f"  [mod] {out.relative_to(DOCS_DIR)}  ->  ::: {module}")
        all_docs.append(out)

    if not all_docs:
        print("\n[WARN] No modules found — nothing generated.")
        return

    # Index
    index_path = generate_index(all_docs)
    print(f"\n  [idx] {index_path.relative_to(DOCS_DIR)}")

    # mkdocs.yml nav
    print()
    update_mkdocs_nav([index_path] + all_docs)

    print(f"\n[OK] Generated {len(all_docs) + 1} docs in {DOCS_DIR}/")


if __name__ == "__main__":
    main()