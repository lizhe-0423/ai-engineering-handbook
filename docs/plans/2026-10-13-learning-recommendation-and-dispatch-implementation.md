# Learning Recommendation and Agent Dispatch Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为个性化学习、学生档案和人工坐席三篇文章补充必要流程图，并写出可落地的推题算法与坐席调度演进方案。

**Architecture:** 推题使用多路候选、硬过滤、可解释排序和约束重排。坐席调度使用状态路由、技能组队列、容量预占和至少一次消息处理，数据库保留归属事实，Redis 与 MQ 分别承担排队加速和事件传递。

**Tech Stack:** Markdown、Mermaid、Git、项目现有中文文风检查脚本

---

### Task 1: 补充个性化推题算法

**Files:**
- Modify: `education-solutions/digital-teacher/personalized-learning.md`

**Step 1: 加入推荐流水线图**

在推荐约束与评测内容之后加入 Mermaid 图，展示学情报告、学生档案和题目特征怎样进入候选召回、硬过滤、排序、重排和反馈更新。

**Step 2: 说明可迁移的大厂结构**

用公开资料说明 Meta、YouTube、X 与 TikTok 的多阶段推荐、信号权重、过滤和多样性做法。明确教育推题借用系统结构，不使用停留时长或点击率作为最终目标。

**Step 3: 写出第一版推题公式**

定义知识缺口、复习紧迫度、难度匹配、目标相关性、探索价值和重复惩罚。公式只表示可以配置与回放的基线，不编造固定权重或统一正确率区间。

**Step 4: 接入学情报告与 Markdown 档案**

学情报告提供高频统计状态，学生档案提供经过确认的慢变量，题库提供可计算的题目特征。说明自由文本需要先读取允许的固定章节，不能直接让整份档案替代排序特征。

**Step 5: 说明模型演进**

先用规则打分验证数据与目标，样本充足后再引入 Learning to Rank、双塔召回或知识追踪模型。大语言模型负责错误线索与解释，不独占最终排序。

### Task 2: 增加学生档案更新图

**Files:**
- Modify: `education-solutions/digital-teacher/student-profile-memory.md`

**Step 1: 增加记忆分层流程图**

展示最近对话、工作摘要、会话总结、候选记忆、档案校验和 `profile.md` 的关系。

**Step 2: 画出分支边界**

明确临时状态继续留在会话层，缺少证据的判断进入待验证区域，确认信息才更新长期档案。版本冲突返回重新读取与重算补丁。

### Task 3: 完善人工坐席调度

**Files:**
- Modify: `education-solutions/digital-teacher/human-handoff.md`

**Step 1: 对比两种调度方案**

保留 Redis 公平队列作为中小规模初期方案，说明它能提供技能组内 FIFO。再介绍以坐席技能、在线状态、瞬时容量和当日容量为中心的路由方案。

**Step 2: 加入混合调度流程图**

展示用户转人工、技能组匹配、可用坐席筛选、容量路由、Redis 排队、容量变化事件、预占、确认和超时回队。

**Step 3: 修正公平分配口径**

当坐席容量不同，基础负载使用当前接待数除以并发上限。负载相同后再比较空闲时间、当日接待比例和会话连续性。说明当日配额需要结合有效工作时长。

**Step 4: 说明 Redis 的职责**

ZSet 保存技能组内的等待顺序与优先级索引。指出 `ZPOPMIN` 只保证取出动作原子，取出、占容量和写归属仍需预占租约、条件更新与超时补偿。

**Step 5: 增加 MQ 可靠性时序图**

画出转人工接口、数据库与 Outbox、发布器、MQ、分配服务、Redis 和坐席端之间的交互。包含重复投递、幂等命中、确认超时和重新排队。

**Step 6: 保持文章边界**

不展开客服工作台缓存、虚拟列表和消息组件拆分。它们属于前端工作台设计。

### Task 4: 验证文章与图表

**Files:**
- Verify: `education-solutions/digital-teacher/personalized-learning.md`
- Verify: `education-solutions/digital-teacher/student-profile-memory.md`
- Verify: `education-solutions/digital-teacher/human-handoff.md`
- Verify: `docs/plans/2026-10-13-learning-recommendation-and-dispatch-implementation.md`

**Step 1: 检查 Mermaid 代码块**

Run: `rg -n '```mermaid|flowchart|sequenceDiagram' education-solutions/digital-teacher/*.md`

Expected: 三篇目标文章共出现四个 Mermaid 代码块，节点名称与正文术语一致。

**Step 2: 运行中文文风检查**

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py education-solutions/digital-teacher/personalized-learning.md`

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py education-solutions/digital-teacher/student-profile-memory.md`

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py education-solutions/digital-teacher/human-handoff.md`

Expected: 不存在阻断发布的翻案句、黑话、冒号和破折号问题。

**Step 3: 检查 Markdown 差异**

Run: `git diff --check`

Expected: 无空白错误。

**Step 4: 检查外部链接与隐私边界**

确认公开资料链接指向 Meta、Google、X、TikTok、Duolingo、哔哩哔哩、Redis、Kafka 与 Debezium 的原文或官方文档。检查文章不包含作者任职公司的名称、内部数据和未公开流程。

**Step 5: 提交文档**

只暂存本轮计划与三篇文章，保留 `.idea/`。提交前确认当前分支不是 `main` 或 `master`。
