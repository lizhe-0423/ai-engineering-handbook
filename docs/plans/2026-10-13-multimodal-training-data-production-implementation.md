# Multimodal Training Data Production Article Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 写成一篇介绍多模态训练数据怎样经过标注、质检、归档并完成训练交付的工程经验文章。

**Architecture:** 正文沿单一生命周期推进，以匿名项目场景承载问题，用公开的一手资料核对标注对象、数据版本和数据血缘等通用做法。文章只使用两张 Mermaid，分别解释生命周期与归档时序。

**Tech Stack:** Markdown、Mermaid、Git、公开产品与开源项目官方文档

---

### Task 1: 核对公开资料

**Files:**
- Reference: `docs/plans/2026-10-13-multimodal-training-data-production-design.md`

**Step 1: 核对标注任务、人工结果与模型预测的对象边界**

查阅数据标注平台官方文档，确认任务、人工标注、模型预测和模型版本之间的关系。

**Step 2: 核对数据集版本与血缘记录**

查阅数据版本或机器学习元数据的官方文档，确认数据来源、摘要、版本和上下游执行关系的通用做法。

**Step 3: 筛选正文引用**

只保留直接支撑文章判断的一手资料，把链接放到相关段落，不建立参考资料列表。

### Task 2: 写作正文与图解

**Files:**
- Create: `enterprise-ai-platform/data-foundation/multimodal-training-data-production.md`

**Step 1: 从交付前的检查问题开篇**

说明文件上传和标注完成仍不足以形成训练数据，训练任务需要引用可重现的数据版本。

**Step 2: 解释数据标注在 AI 产品中的作用**

说明常见标注任务、岗位门槛、外部人员与内部团队的分工，以及图像模型和大模型采用不同标注形式的原因。

**Step 3: 写出数据生产生命周期**

加入一张 Mermaid 流程图，覆盖素材接入、数据集版本、标注、质检、归档与训练交付，并保留退回返工分支。

**Step 4: 解释数据对象与结果来源**

区分文件、样本、数据集、数据集版本、标注任务和标注结果。用 AI 预标注、标签映射和 DPO 偏好样本作为简短例子。

**Step 5: 解释质检与返工**

说明抽样范围、判定结果、问题类型、退回与复检需要留痕，避免只保存一个通过率。

**Step 6: 解释归档时序**

加入一张 Mermaid 时序图，展示冻结清单、完整性校验、生成只读版本、记录血缘和通知下游的顺序。

**Step 7: 补充异步任务与失败处理**

说明导入、预标注、导出和归档为什么适合异步执行，以及任务幂等、重试、补偿和对账的边界。

**Step 8: 写明训练交付与后续修订**

说明导出格式、训练集划分、版本引用和复制修订的关系，避免修改已经被训练任务引用的归档版本。

### Task 3: 增加目录入口

**Files:**
- Modify: `enterprise-ai-platform/data-foundation/README.md`

**Step 1: 更新目录说明**

把文章入口放在数据工程与智能标注目录中，摘要覆盖标注、质检、归档和训练交付。

**Step 2: 检查相邻文章边界**

确认新文章不重复 CDC 的变更捕获内容，也不展开数据反馈系统的评测闭环。

### Task 4: 完成编辑与验证

**Files:**
- Verify: `enterprise-ai-platform/data-foundation/multimodal-training-data-production.md`
- Verify: `enterprise-ai-platform/data-foundation/README.md`

**Step 1: 执行中文文章检查**

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py enterprise-ai-platform/data-foundation/multimodal-training-data-production.md`

Expected: 硬性禁用项均为 0。

**Step 2: 检查 Markdown 与 Mermaid**

Run: `git diff --check`

Expected: 无输出，退出码为 0。

确认 Mermaid 代码块数量为 2，代码围栏成对出现，本地链接目标存在。

**Step 3: 检查脱敏边界**

搜索截图中的公司名、人员名、数据集名称、系统地址和业务数字。

Expected: 正文不包含这些内容。

**Step 4: 检查 Git 范围**

Run: `git status --short`

Expected: 只包含设计稿、实施计划、新文章和目录修改，`.idea/` 保持未跟踪且不进入暂存区。

### Task 5: 整理本地提交

**Files:**
- Add: `docs/plans/2026-10-13-multimodal-training-data-production-design.md`
- Add: `docs/plans/2026-10-13-multimodal-training-data-production-implementation.md`
- Add: `enterprise-ai-platform/data-foundation/multimodal-training-data-production.md`
- Modify: `enterprise-ai-platform/data-foundation/README.md`

**Step 1: 复核差异**

Run: `git diff --stat origin/docs/ai-education-scenarios...HEAD`

Expected: 仅包含本次文章相关文件。

**Step 2: 整理为一个本地工作提交**

把设计、计划、正文和目录修改整理成一个提交，不推送远端，等待用户确认。

**Step 3: 提交后再次验证**

Run: `git show --check --stat --oneline HEAD`

Expected: 提交检查通过，作者使用仓库本地配置的个人 Git 身份。
