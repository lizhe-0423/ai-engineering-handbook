# AI Native Overview Article Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Publish the first AI Native article and replace the section placeholder with a concise navigation page.

**Architecture:** Store the standalone article at `ai-native/what-ai-native-changes.md` and link it from `ai-native/README.md`. Use one Mermaid flowchart and one comparison table to explain the workflow and keep later infrastructure topics outside this article.

**Tech Stack:** Markdown, Mermaid, relative links

---

### Task 1: Write the overview article

**Files:**
- Create: `ai-native/what-ai-native-changes.md`

**Step 1: Write the concrete opening**

Start from a small repository task and show why generating a code fragment does not complete the engineering task.

**Step 2: Explain the four engineering changes**

Cover task contracts, context assembly, verification, and runtime governance. Define each term when it first appears.

**Step 3: Add the visual explanation**

Add a Mermaid flowchart for the controlled execution path and a table comparing traditional automation, AI-assisted coding, and AI Native development.

**Step 4: State the boundary**

Explain which decisions remain in deterministic services or human approval, then point readers to later Harness and runtime articles without creating empty links.

### Task 2: Replace the section placeholder

**Files:**
- Modify: `ai-native/README.md`

**Step 1: Remove the research declaration**

Delete the source-description paragraph and the future-writing statement.

**Step 2: Add the completed article entry**

Keep a short section description and link to `what-ai-native-changes.md`.

### Task 3: Verify and commit

**Files:**
- Verify: `ai-native/README.md`
- Verify: `ai-native/what-ai-native-changes.md`

**Step 1: Run prose checks**

Run the human-writing checker on both publishable files and resolve required changes.

**Step 2: Check Markdown and links**

Run `git diff --check` and verify every relative Markdown target exists.

**Step 3: Inspect Mermaid source**

Check that every decision node has an outgoing path and the diagram contains no unsupported syntax.

**Step 4: Commit**

Stage the two publishable files and this implementation plan, then commit with `docs: add AI Native overview article`.
