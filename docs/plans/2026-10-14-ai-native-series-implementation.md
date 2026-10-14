# AI Native Article Series Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Complete the AI Native section with six standalone engineering articles and a finished navigation page.

**Architecture:** Keep each topic in one Markdown file under `ai-native/`. Reuse a concrete engineering task inside each article, add one Mermaid diagram where relationships need visual explanation, and leave vendor-specific products outside the main argument.

**Tech Stack:** Markdown, Mermaid, relative links, Chinese prose checker

---

### Task 1: Explain Agent Harness through a long-running task

**Files:**
- Create: `ai-native/agent-harness-long-running-task.md`

**Step 1: Write the task walkthrough**

Start with a failed build repair. Follow the task through context loading, planning, tool calls, observation, verification and completion.

**Step 2: Explain state and recovery**

Describe checkpoints, retry boundaries, resumable state and human approval without expanding into Sandbox or identity implementation.

**Step 3: Add the sequence diagram**

Use one Mermaid sequence diagram to distinguish the user, Harness, model, tool service and verifier.

**Step 4: Verify and commit**

Run the prose checker, `git diff --check`, link checks and Mermaid block checks. Commit as `docs: explain Agent Harness execution`.

### Task 2: Explain enterprise context and tools

**Files:**
- Create: `ai-native/enterprise-context-and-tools.md`

**Step 1: Separate information from action**

Explain project rules, enterprise knowledge, Skill, MCP and CLI through one dependency-upgrade task.

**Step 2: Define tool contracts**

Cover capability discovery, typed inputs, outputs, side effects, permissions, idempotency and evidence.

**Step 3: Add the layered flow diagram**

Use one Mermaid diagram to show how rules, knowledge, task methods and execution tools enter the Harness.

**Step 4: Verify and commit**

Run the standard document checks. Commit as `docs: explain Agent context and tools`.

### Task 3: Explain the Agent runtime environment

**Files:**
- Create: `ai-native/agent-runtime-environment.md`

**Step 1: Follow a task environment lifecycle**

Explain image selection, workspace creation, dependency setup, execution, artifact collection and environment disposal.

**Step 2: Separate Sandbox and Coding Environment**

Describe isolation and resource policy as Sandbox responsibilities, and repository, dependencies, editor services and test tools as Coding Environment responsibilities.

**Step 3: Add the lifecycle diagram**

Use one Mermaid state diagram with success, failure, timeout and recovery paths.

**Step 4: Verify and commit**

Run the standard document checks. Commit as `docs: explain Agent runtime environments`.

### Task 4: Explain identity, policy and Guardrail

**Files:**
- Create: `ai-native/agent-identity-policy-guardrail.md`

**Step 1: Trace one protected operation**

Use a deployment-configuration change to show user identity, Agent identity, delegated credentials and downstream authorization.

**Step 2: Explain policy enforcement**

Cover least privilege, short-lived credentials, tool-side checks, dynamic approval and input or output Guardrails.

**Step 3: Add the authorization sequence**

Use one Mermaid sequence diagram that shows where a request can be blocked or sent for approval.

**Step 4: Verify and commit**

Run the standard document checks. Commit as `docs: explain Agent identity and safety`.

### Task 5: Explain observability and evaluation

**Files:**
- Create: `ai-native/agent-observability-and-evaluation.md`

**Step 1: Reconstruct a failed execution**

Explain run, trace and span records, then distinguish model, tool, environment, policy and verification failures.

**Step 2: Connect offline and online evaluation**

Cover task success, tool selection, first-pass success, retries, human intervention, cost and latency. Explain why one aggregate score is insufficient.

**Step 3: Add the trace diagram**

Use one Mermaid diagram to show a task trace and the evidence attached to each step.

**Step 4: Verify and commit**

Run the standard document checks. Commit as `docs: explain Agent observability and evaluation`.

### Task 6: Explain team adoption and finish navigation

**Files:**
- Create: `ai-native/agent-team-adoption.md`
- Modify: `ai-native/README.md`

**Step 1: Explain task routing and ownership**

Separate scripted automation, supervised Agent work and autonomous Agent work. Define who owns goals, constraints, review and incidents.

**Step 2: Explain how to measure adoption**

Use lead time, review load, rework, escaped defects and human takeover to assess whether Agent use actually helps the team.

**Step 3: Add the task-routing diagram**

Use one Mermaid decision diagram that routes work by determinism, risk and verification cost.

**Step 4: Complete the section navigation**

List all finished articles in reading order and replace the future-topic table with a compact completed map.

**Step 5: Run full-section verification and commit**

Run prose checks for every article, verify every relative link, inspect all Mermaid blocks and run `git diff --check`. Commit as `docs: complete AI Native article series`.

### Task 7: Finish the completed series

**Files:**
- Verify: `ai-native/*.md`
- Verify: `docs/plans/2026-10-14-ai-native-series-*.md`

**Step 1: Review the complete change set**

Confirm the branch is `dev`, `.idea/` and temporary PDF files are not staged, and no internal company information appears in the articles.

**Step 2: Remove research files**

Delete `tmp/pdfs/` after all source checks are complete.

**Step 3: Run fresh verification**

Run the prose checker, relative-link checks, Mermaid checks and `git show --check` for the latest commits.

**Step 4: Prepare the handoff**

Report the local commits and verification results. Do not push until the user gives a new explicit remote-write instruction.
