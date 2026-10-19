# Student Profile Memory Article Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 新增一篇讲清学生 Markdown 档案、会话压缩与长期记忆更新的教育 AI 工程文章。

**Architecture:** 学习事件、当前会话、会话摘要和长期档案分层保存。学生档案通过学生编号确定性读取，不建立向量索引；AI 生成受约束的更新补丁，普通服务负责版本、权限与审计。

**Tech Stack:** Markdown、Git、项目现有中文文风检查脚本

---

### Task 1: 新增学生档案长期记忆文章

**Files:**
- Create: `education-solutions/digital-teacher/student-profile-memory.md`

**Step 1: 说明为什么不使用向量检索**

从已知学生、已知档案路径和较小文件规模出发，解释确定性读取、固定章节与精确搜索为什么更合适，同时保留 RAG 在教材和教师资料中的用途。

**Step 2: 设计 Markdown 档案结构**

给出包含版本、更新时间、学习目标、讲解偏好、薄弱点、待验证判断和未完成任务的示例。说明 Markdown 是格式，生产存储仍需权限、版本和审计。

**Step 3: 区分短期记忆、会话摘要和长期档案**

说明最近几轮原文、窗口压缩摘要、会话结束总结和 `profile.md` 的不同职责，以及运行时的加载顺序。

**Step 4: 说明档案更新策略**

覆盖学生或教师明确修改、会话结束后的主动整理、重复证据、待验证判断、过期与冲突。AI 只生成补丁，业务服务检查后写入新版本。

**Step 5: 说明评测与隐私边界**

检查错误记忆、过期信息、版本冲突、压缩丢失和越权加载。档案只保存教学相关信息，不写家庭、情绪和生活经历。

### Task 2: 衔接现有个性化学习文章

**Files:**
- Modify: `education-solutions/digital-teacher/personalized-learning.md`

**Step 1: 修正 Agent 更新边界**

把“Agent 不直接修改学生档案”补充为“Agent 可以生成更新建议，档案服务负责验证和写入”，并链接到新文章。

**Step 2: 保持原文章主线**

不在原文展开 Markdown、上下文压缩和文件版本，继续围绕学习事件、掌握度和推荐约束写作。

### Task 3: 更新导航并验证

**Files:**
- Modify: `education-solutions/digital-teacher/README.md`
- Modify: `education-solutions/README.md`
- Verify: `education-solutions/digital-teacher/student-profile-memory.md`

**Step 1: 加入两级目录导航**

数字名师目录增加学生档案文章，教育解决方案总目录在数字名师条目中补充长期记忆内容。

**Step 2: 运行文风检查**

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py education-solutions/digital-teacher/student-profile-memory.md`

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py education-solutions/digital-teacher/personalized-learning.md`

Expected: 不存在阻断发布的文风问题。

**Step 3: 检查 Markdown 与敏感信息**

Run: `git diff --check`

Expected: 无空白错误。

Run: `rg -n "家庭情况|情绪经历|生活经历|学生档案向量库" education-solutions/digital-teacher/student-profile-memory.md`

Expected: 正文只在边界说明中提及不应保存的信息，不把它们设计成档案字段。

**Step 4: 提交文档**

只暂存本轮文章、导航和计划文件，保留 `.idea/`。提交前核对当前分支不是 `main` 或 `master`。
