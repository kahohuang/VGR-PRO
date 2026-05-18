# VGR Repo Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert this folder into a code-only Git repository and reduce the monolithic assistant script into smaller Python modules without changing current behavior.

**Architecture:** Keep Python as the source of truth for workbook analysis, message generation, and dashboard rendering. Introduce a small package with focused modules plus a thin compatibility entrypoint so the existing batch launcher and imports continue to work.

**Tech Stack:** Python, `openpyxl`, `unittest`, static HTML/JS output

---

### Task 1: Define repository boundaries

**Files:**
- Create: `.gitignore`
- Modify: `README_VGR_AI助手.md`

- [ ] Add ignore rules for business data, generated output, caches, and local dependencies.
- [ ] Update the README so it explains that Git only tracks code and AI-authored project documents.

### Task 2: Split the monolithic script

**Files:**
- Create: `vgr_assistant/__init__.py`
- Create: `vgr_assistant/models.py`
- Create: `vgr_assistant/analysis.py`
- Create: `vgr_assistant/messaging.py`
- Create: `vgr_assistant/reporting.py`
- Create: `vgr_assistant/dashboard.py`
- Create: `vgr_assistant/cli.py`
- Modify: `vgr_ai_assistant.py`

- [ ] Move data structures and constants into `models.py`.
- [ ] Move workflow classification and workbook loading into `analysis.py`.
- [ ] Move English message generation into `messaging.py`.
- [ ] Move CSV, Markdown, and dashboard file-writing helpers into reporting modules.
- [ ] Keep `vgr_ai_assistant.py` as a compatibility shim that re-exports public functions and calls the new CLI entrypoint.

### Task 3: Verify behavior and initialize Git

**Files:**
- Modify: `tests/test_vgr_ai_assistant.py` if import paths need compatibility coverage

- [ ] Run the existing unit tests against the refactored structure.
- [ ] Remove disposable cache/output folders from the workspace.
- [ ] Initialize Git after the ignore rules are in place.
