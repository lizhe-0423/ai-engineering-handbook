# Digital Teacher Q&A Articles Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 完善数字名师答疑文章，并新增一篇独立的在线人工答疑与坐席调度文章。

**Architecture:** 数字名师文章覆盖知识库、意图判断、固定题库拍搜、受控回答和拒答。人工答疑文章覆盖会话接管与坐席调度，两篇通过目录导航关联，但不把人工接管设为数字名师 Agent 的必经节点。

**Tech Stack:** Markdown、Git、项目现有中文文档校验脚本

---

### Task 1: 完善数字名师答疑文章

**Files:**
- Modify: `education-solutions/digital-teacher/qa.md`

**Step 1: 保留现有问题入口**

保留拍照输入不规范、题干残缺和追问缺少上下文等真实问题，避免把文章改成抽象架构说明。

**Step 2: 补充名师知识库与会话判断**

说明课件、逐字稿、音频转写和教师介绍的入库方式，以及首次会话与会话中期的意图判断边界。

**Step 3: 加入固定题库拍搜流程**

以“某专升本公司”为脱敏案例，写清图像识别、候选题召回、相似图片展示、用户确认、AI 讲解和错误反馈。

**Step 4: 删除实时转人工分支**

把高风险、连续低置信和资料冲突改为打标、澄清或拒答。反馈只进入异步复核与题库维护任务。

### Task 2: 新增在线人工答疑文章

**Files:**
- Create: `education-solutions/digital-teacher/human-handoff.md`

**Step 1: 定义主动转人工与人工接管**

说明入口、会话状态、上下文快照和机器人暂停条件。

**Step 2: 说明坐席状态与公平分配**

使用接待上限、排队时长和当前负载描述可执行的分配策略。

**Step 3: 说明消息队列的一致性边界**

写清至少一次投递、业务幂等、会话租约、确认、重试、死信和回收机制，避免承诺不存在的“绝不重复”。

**Step 4: 说明故障恢复和验收指标**

覆盖坐席离线、进程崩溃、租约过期、重复消息与积压场景。

### Task 3: 更新目录并校验

**Files:**
- Modify: `education-solutions/digital-teacher/README.md`
- Verify: `education-solutions/digital-teacher/qa.md`
- Verify: `education-solutions/digital-teacher/human-handoff.md`

**Step 1: 更新目录导航**

删除“分步讲解和转人工”，分别列出数字名师答疑与在线人工答疑文章。

**Step 2: 运行中文文风检查**

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py education-solutions/digital-teacher/qa.md`

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py education-solutions/digital-teacher/human-handoff.md`

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py education-solutions/digital-teacher/README.md`

Expected: 不存在阻断发布的文风问题。

**Step 3: 检查 Markdown 与敏感信息**

Run: `git diff --check`

Expected: 无空白错误。

Run: `rg -n "客户名称|内部地址|转给真人|转给教师" education-solutions/digital-teacher`

Expected: 不出现真实公司或客户信息，数字名师文章不包含自动转人工分支。

**Step 4: 提交并发布文档分支**

只暂存本轮文档，保留 `.idea/`。发布前重新获取 `origin/main`，线性变基并再次校验，随后只推送 `docs/ai-education-scenarios`。
