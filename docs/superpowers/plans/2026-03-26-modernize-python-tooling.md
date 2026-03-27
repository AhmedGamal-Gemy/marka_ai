# Modernize Python Tooling (uv & pyproject.toml) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the project's tooling from standard `pip`/`venv` to use `uv` for dependency management and environment isolation, centralized within a `pyproject.toml` configuration file, and update `GEMINI.md` to reflect these changes along with helpful PowerShell commands.

**Architecture:** The project will utilize a declarative `pyproject.toml` file to manage dependencies and configurations for tools like `pytest`, `ruff`, and `mypy`. The instructions in `GEMINI.md` will be updated to guide developers on using `uv` to sync environments and run scripts, replacing the old `venv` and `pip` instructions.

**Tech Stack:** `uv`, `pyproject.toml`, Markdown

---

### Task 1: Initialize pyproject.toml with uv

**Files:**
- Create: `pyproject.toml`

- [ ] **Step 1: Create a basic `pyproject.toml` using `uv`**

Run: `uv init --app --no-workspace`
Expected: `uv` initializes a new `pyproject.toml` and potentially a `.python-version` file. It might also create a `hello.py` or similar default file which we should clean up if not needed, but for now, we focus on the `pyproject.toml`.

- [ ] **Step 2: Add standard development dependencies**

Run: `uv add --dev ruff mypy pytest`
Expected: `uv` updates `pyproject.toml` with the `[dependency-groups.dev]` section including the requested tools, and generates a `uv.lock` file.

- [ ] **Step 3: Add core backend dependencies**

Run: `uv add fastapi pydantic python-telegram-bot "litellm[proxy]"`
Expected: `uv` updates the `[project.dependencies]` section in `pyproject.toml`.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "build: initialize pyproject.toml and add base dependencies with uv"
```

### Task 2: Update GEMINI.md - Building and Running Section

**Files:**
- Modify: `GEMINI.md:32-42`

- [ ] **Step 1: Replace pip/venv instructions with uv in `GEMINI.md`**

In `GEMINI.md`, locate the following block (around line 32):
```markdown
**For Python Development (AI Layer):**
```bash
# 1. Environment Setup
python -m venv .venv
# source .venv/bin/activate (Linux/macOS)
# .venv\Scripts\activate (Windows)

# 2. Tooling Installation
pip install ruff mypy pytest
```
```

Replace it entirely with:

```markdown
**For Python Development (AI Layer):**
This project uses `uv` for fast Python dependency and environment management.

```bash
# 1. Install dependencies and create the virtual environment
uv sync

# 2. Add a new package
uv add <package_name>

# 3. Add a development dependency
uv add --dev <package_name>
```

**Note:** You do not need to manually activate the virtual environment if you prefix your commands with `uv run` (e.g., `uv run python main.py`).
```

- [ ] **Step 2: Review the changes**

Run: `git diff GEMINI.md`
Expected: Only the "Building and Running" section should be modified, replacing `pip`/`venv` with `uv` instructions.

- [ ] **Step 3: Commit**

```bash
git add GEMINI.md
git commit -m "docs: update GEMINI.md to use uv for dependency management"
```

### Task 3: Update GEMINI.md - Add PowerShell & Testing Sections

**Files:**
- Modify: `GEMINI.md:43-` (Append before the 'Development Conventions' section or at the end of the 'Building and Running' section)

- [ ] **Step 1: Add a Testing section to `GEMINI.md`**

Insert the following section right after the newly updated "Building and Running" block in `GEMINI.md`:

```markdown
## 🧪 Testing

Run tests using `pytest` via `uv`:

```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_chatbot.py

# Run tests matching a specific string
uv run pytest -k "test_intent"

# Run tests with verbose output
uv run pytest -v
```
```

- [ ] **Step 2: Add a PowerShell Productivity section to `GEMINI.md`**

Insert the following section directly below the new "Testing" block:

```markdown
## ⚡ PowerShell Productivity

Helpful commands for Windows development:

```powershell
# Set an environment variable for the current session
$env:OPENAI_API_KEY="your-key-here"

# Quickly search for a string across all Python files
Select-String -Pattern "class ChatbotAgent" -Path "*.py" -Recurse

# Stop a runaway Python process
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force
```
```

- [ ] **Step 3: Review the changes**

Run: `git diff GEMINI.md`
Expected: The new "Testing" and "PowerShell Productivity" sections are present and correctly formatted.

- [ ] **Step 4: Commit**

```bash
git add GEMINI.md
git commit -m "docs: add testing and PowerShell productivity commands to GEMINI.md"
```
