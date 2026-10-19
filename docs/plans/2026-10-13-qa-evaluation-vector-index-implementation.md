# QA Evaluation and Vector Index Governance Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为数字名师补齐可插拔 Agent 流程、检索评测与人工兜底，并新增一篇可落地的数据库与向量索引治理文章。

**Architecture:** `qa.md` 保持实时答题主线，只解释节点编排、分层评测与业务兜底。向量索引的增量同步、全量重建、去重、灰度、备份和数据飞轮放到企业级 AI 生产平台，业务数据是事实源，向量库是可重建索引。

**Tech Stack:** Markdown、Mermaid、Git、项目现有中文文风检查脚本

---

### Task 1: 增加受控 Agent 流程图

**Files:**
- Modify: `education-solutions/digital-teacher/qa.md`

**Step 1: 补充节点分类**

在“Agent 负责串起受控流程”中明确必经节点与可选节点。必经节点包括状态读取、范围判断、输出检查和最终出口。图片 OCR、同题搜索、教师知识检索、计算工具与重排按输入和状态启用。

**Step 2: 增加 Mermaid 图**

使用 `classDef required` 和 `classDef optional` 区分两类节点。流程包含文本与图片分支、同题命中、RAG 候选、工具校验、回答检查和拒答。

**Step 3: 写出插件契约**

说明每个可选节点需要声明输入、输出、版本、超时、错误码、失败出口和允许读写的状态。增加新节点通过配置与统一契约完成，不改写主流程的安全边界。

### Task 2: 扩展检索评测与业务兜底

**Files:**
- Modify: `education-solutions/digital-teacher/qa.md`

**Step 1: 区分三类检索目标**

同题拍搜看标准原题的排名，相似题推荐看多个相关项的排序，教师知识库看多个片段的覆盖与噪声。

**Step 2: 解释评测指标**

增加一张表格，解释 `Top1 Accuracy`、`Hit@K`、`Recall@K`、`Precision@K`、`MRR@K` 和 `nDCG@K` 的计算含义、适合场景与局限。

增加 MRR 小例子。三条测试查询的第一个正确结果分别在第一、第二与未命中位置，平均倒数排名为 `(1 + 1/2 + 0) / 3` 。

**Step 3: 拆开检索和回答评测**

检索评测完成后，再单独检查结论正确、关键步骤、引用支持、引用完整、提示深度和拒答边界。不用单一总分遮住不同失败原因。

**Step 4: 加入传统人工兜底**

说明未命中、错命中与资料冲突如何进入运营复核队列。运营人员先修改标准题和题目关系，再由同步流程更新索引。学生当前请求使用已审核答案、教师预设题包或拒答作为兜底。

### Task 3: 新增向量索引生命周期文章

**Files:**
- Create: `enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md`

**Step 1: 界定事实源与索引**

说明业务数据库保存题目实例、版本、来源、状态和审计记录。向量点保存 `entity_id`、`entity_version`、`content_hash`、`embedding_model_version`、`index_version` 与可过滤元数据，可以从业务数据重建。

**Step 2: 写增量同步**

业务事务同时写入 Outbox，或使用 CDC 读取已提交更改。索引器幂等处理 upsert 与 tombstone，用单调版本拒绝迟到事件，定期以业务库为准对账。

**Step 3: 写全量重建与灰度迁移**

用 Mermaid 图展示高水位快照、新集合后台构建、增量重放、完整性检查、检索评测、影子读、灰度、原子切换和回滚。说明全量任务限速、资源隔离与可恢复进度。

**Step 4: 写题库去重模型**

区分题目实例、标准题与题目关系。完全一致使用归一化哈希，近似候选结合关键词、shingle、向量与图片特征。复核标签使用同题、变式题、同知识点和不相关。保留试卷、页码与考试批次中的每个题目实例。

**Step 5: 写删除、备份与回滚**

业务逻辑删除先让向量点变为不可检索，保留期结束后再物理删除。迁移前保留快照或可重建源数据，旧索引在观察期继续接收增量，保证能够切回。

**Step 6: 写数据飞轮**

用 Mermaid 图展示线上反馈、失败样本、人工复核、业务数据修正、增量索引、候选评测集、固定回归集、离线比较与灰度发布。明确训练数据与同版评测集分离。

### Task 4: 补齐导航和文章关联

**Files:**
- Modify: `enterprise-ai-platform/knowledge-engineering/README.md`
- Modify: `education-solutions/digital-teacher/qa.md`

**Step 1: 增加知识工程入口**

在知识工程 README 增加文章链接，摘要包含增量同步、全量重建、去重、灰度和评测集。

**Step 2: 从答疑文章连到系统能力**

在题库人工兜底附近增加相对链接，不在 `qa.md` 重复数据迁移细节。

### Task 5: 验证与提交

**Files:**
- Verify: `education-solutions/digital-teacher/qa.md`
- Verify: `enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md`
- Verify: `enterprise-ai-platform/knowledge-engineering/README.md`
- Verify: `docs/plans/2026-10-13-qa-evaluation-vector-index-design.md`
- Verify: `docs/plans/2026-10-13-qa-evaluation-vector-index-implementation.md`

**Step 1: 检查 Mermaid 代码块**

Run: `rg -n '\`\`\`mermaid|flowchart|classDef' education-solutions/digital-teacher/qa.md enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md`

Expected: 两篇文章共有三个 Mermaid 代码块，Agent 图包含必经与可选节点样式。

**Step 2: 运行中文文风检查**

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py education-solutions/digital-teacher/qa.md`

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md`

Expected: 无翻案句、硬停词、黑话和违规标点阻断项。

**Step 3: 检查指标与业务规则**

Run: `rg -n 'Top1 Accuracy|Hit@K|Recall@K|Precision@K|MRR@K|nDCG@K|tombstone|entity_version|embedding_model_version' education-solutions/digital-teacher/qa.md enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md`

Expected: 检索指标、版本字段与删除事件都有明确说明。

**Step 4: 检查隐私与 Markdown 差异**

Run: `rg -n '师大|真实客户|系统地址|内部表|供应商配置' education-solutions/digital-teacher/qa.md enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md`

Expected: 无匹配。

Run: `git diff --check`

Expected: 无空白错误。

**Step 5: 提交并发布**

只暂存两篇文章、知识工程导航与两份计划，保留 `.idea/`。把本轮开发整理为一个本地提交。推送前获取远端最新状态，确认分支、上游、工作区、源 SHA 与目标引用，目标只能是 `refs/heads/docs/ai-education-scenarios`。
