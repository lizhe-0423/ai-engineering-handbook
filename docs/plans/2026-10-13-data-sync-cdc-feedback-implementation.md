# Data Sync, CDC, and Feedback Systems Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 把题库向量同步、CDC 数据采集和数据反馈评测拆成三个边界清楚、互相链接的工程主题。

**Architecture:** 单体题库默认使用本地事务任务表、MQ、幂等消费、失败补偿和定期对账。CDC 作为复杂数据接入方案独立成篇，数据反馈与评测作为横向平台系统独立成篇，审核结果通过业务事实数据与标准同步流程重新进入产品。

**Tech Stack:** Markdown、Mermaid、Git、项目现有中文文风检查脚本

---

### Task 1: 调整向量索引的默认同步方案

**Files:**
- Modify: `enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md`

**Step 1: 重写增量同步入口**

把 CDC 从默认流程移出。说明题目修改和同步任务写入同一本地事务，任务发布器再把消息投递到 MQ。

**Step 2: 增加同步任务字段**

列出 `task_id`、`entity_id`、`entity_version`、`event_type`、`status`、`retry_count`、`next_retry_at` 和 `last_error`。解释单个 `is_synced` 无法表示多版本、多索引和失败状态。

**Step 3: 增加同步时序图**

使用 Mermaid `sequenceDiagram` 展示业务事务、任务发布器、MQ、索引消费者、业务数据库和向量索引之间的交互。图中包含发布失败重试、消费者读取最新版本、幂等 upsert 与完成状态。

**Step 4: 区分重新计算向量与元数据更新**

题干、选项或参与 embedding 的答案发生变化时重新计算向量。来源、审核状态和上下架状态只更新 payload 或过滤字段。使用 `content_hash` 跳过无意义的重复计算。

**Step 5: 增加方案选择表**

比较同步任务表加 MQ、RocketMQ 事务消息、CDC 加 MQ和全量快照加增量重放。CDC 只保留摘要与新文章链接。

### Task 2: 新增 CDC 工程方案

**Files:**
- Create: `enterprise-ai-platform/data-foundation/cdc-change-capture.md`

**Step 1: 解释 CDC 的职责**

说明 CDC 从数据库提交日志捕获变化，可以用于搜索索引、数仓、数据湖、多下游订阅和跨环境复制。多机房只是其中一种用途。

**Step 2: 增加事务时序图**

使用 Mermaid `sequenceDiagram` 展示业务事务提交、binlog 或 WAL、CDC 连接器、MQ 与下游消费者。未提交事务不能进入下游。

**Step 3: 区分数据库事务与业务事件**

说明 CDC 能识别事务边界并提供事务元数据，行级事件不会自动组合成一个完整业务动作。需要业务语义时使用 Outbox，Outbox 可以由轮询器或 CDC 发布。

**Step 4: 写出生产难点**

覆盖初始快照与增量衔接、位点恢复、重复和乱序、分区顺序、结构变更、大事务、删除事件、日志保留、监控和重放。

**Step 5: 给出适用边界**

明确写入口可控且下游少时优先使用任务表和 MQ。旧系统多写入口、多个下游或需要通用变化流时再采用 CDC。

### Task 3: 新增数据反馈与评测系统

**Files:**
- Create: `enterprise-ai-platform/data-foundation/data-feedback-evaluation.md`

**Step 1: 定义系统边界**

线上业务只产生反馈事件。反馈系统负责采集、去重、抽样、复核、业务修正、数据集登记和评测，不直接修改线上向量。

**Step 2: 设计反馈事件**

说明事件至少保留请求 ID、业务对象、用户输入快照、候选结果、模型与索引版本、用户动作、时间和权限范围。用户点击属于弱信号，人工复核以后才能形成正式标签。

**Step 3: 增加跨系统流程图**

使用 Mermaid `flowchart` 展示线上产品、事件采集、样本治理、人工复核、业务数据库、数据集注册、离线评测和灰度发布。

**Step 4: 管理数据集版本**

区分固定回归集、滚动困难集和训练数据分区。记录来源、标注依据、版本和数据使用范围，避免训练数据泄漏到同版独立评测集。

**Step 5: 写异常处理与运行指标**

覆盖重复反馈、迟到事件、误点、隐私删除、复核积压、标注分歧和版本缺失。运行指标只给计算方向，不编造通用阈值。

### Task 4: 更新导航与跨文链接

**Files:**
- Modify: `enterprise-ai-platform/data-foundation/README.md`
- Modify: `enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md`
- Modify: `enterprise-ai-platform/knowledge-engineering/README.md`

**Step 1: 增加数据工程导航**

在数据工程 README 增加 CDC 与数据反馈两篇文章入口，并写清它们各自处理的问题。

**Step 2: 增加跨文链接**

向量同步文章在复杂变更捕获处链接 CDC 文章，在反馈样本处链接数据反馈文章。

**Step 3: 修正知识工程摘要**

让知识工程 README 对向量索引文章的描述以任务表、MQ、版本同步、全量重建和去重为主，不再把数据飞轮写成文章内部流程。

### Task 5: 验证并发布

**Files:**
- Verify: `enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md`
- Verify: `enterprise-ai-platform/data-foundation/cdc-change-capture.md`
- Verify: `enterprise-ai-platform/data-foundation/data-feedback-evaluation.md`
- Verify: `enterprise-ai-platform/data-foundation/README.md`
- Verify: `enterprise-ai-platform/knowledge-engineering/README.md`

**Step 1: 检查方案边界**

Run: `rg -n '本地事务|同步任务|MQ|CDC|Outbox|幂等|对账|固定回归集|滚动困难集' enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md enterprise-ai-platform/data-foundation/*.md`

Expected: 默认方案、CDC 边界与数据集分区都有明确说明。

**Step 2: 检查 Mermaid**

Run: `rg -n '^```mermaid$|sequenceDiagram|flowchart' enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md enterprise-ai-platform/data-foundation/*.md`

Expected: 三篇文章都包含服务于流程关系的 Mermaid 图，代码围栏成对。

**Step 3: 运行中文文风检查**

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py <article>`

Expected: 三篇文章没有翻案句、硬停词、违规冒号和模型化路标。

**Step 4: 检查隐私与 Markdown**

Run: `rg -n '师大|真实客户|系统地址|内部表|供应商配置|zhaoxi|朝夕' enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md enterprise-ai-platform/data-foundation/*.md`

Expected: 无匹配。

Run: `git diff --check`

Expected: 无空白错误。

**Step 5: 整理并发布提交**

只暂存本轮设计、计划和文章文件，保留 `.idea/`。把本轮提交整理成一个工作提交。获取远端最新状态，确认 `origin/main` 是当前分支祖先，核对源 SHA 与目标引用以后，只推送 `refs/heads/docs/ai-education-scenarios`。
