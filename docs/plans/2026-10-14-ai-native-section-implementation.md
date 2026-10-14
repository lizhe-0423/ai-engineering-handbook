# AI Native Section Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a visible AI Native entry to the repository homepage and create its top-level navigation page.

**Architecture:** Keep the root `README.md` as the global directory and use `ai-native/README.md` as the section landing page. The landing page summarizes the verified structure of Alibaba's official AI Native handbook without copying its chapters or linking to unfinished local articles.

**Tech Stack:** Markdown, relative repository links, official HTTPS source link

---

### Task 1: Create the AI Native landing page

**Files:**
- Create: `ai-native/README.md`

**Step 1: Create the directory page**

Explain the section scope and organize the future content into practice cases, engineering challenges, and enterprise infrastructure.

**Step 2: Add the official source link**

Link to the official online handbook and state that future articles will reorganize the material instead of reproducing it.

**Step 3: Run the prose check**

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py ai-native/README.md`

Expected: zero required changes.

### Task 2: Add the homepage entry

**Files:**
- Modify: `README.md`

**Step 1: Add the topic row**

Add AI Native to the contents table and link it to `ai-native/README.md`.

**Step 2: Verify relative links**

Run a relative Markdown link check for `README.md` and `ai-native/README.md`.

Expected: all local targets exist.

### Task 3: Verify and publish on dev

**Files:**
- Verify: `README.md`
- Verify: `ai-native/README.md`

**Step 1: Check Markdown differences**

Run: `git diff --check`

Expected: no output.

**Step 2: Review the staged change set**

Run: `git status --short` and `git diff --stat`

Expected: only the planned Markdown files and plan document are changed; `.idea/` remains untracked.

**Step 3: Commit**

Run: `git add README.md ai-native/README.md docs/plans/2026-10-14-ai-native-section-implementation.md`

Run: `git commit -m "docs: add AI Native section"`

**Step 4: Push dev**

Run: `git push origin dev`

Expected: `origin/dev` advances to the new documentation commit while `origin/main` remains unchanged.
