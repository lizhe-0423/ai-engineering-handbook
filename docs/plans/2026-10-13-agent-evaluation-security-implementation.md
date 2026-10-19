# Agent 评测与服务安全文章实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在 AI Agent 学习路线中新增评测与生产安全两篇独立文章，并把现有四阶段路线调整为五阶段。

**Architecture:** 保持 `agent-learning-path/` 扁平目录。Agent 评测文章负责版本回归、任务结果验证和评测集维护，Agent 服务安全文章负责能力保护、异常调用识别和分层处置，两篇文章通过安全评测集连接，并链接通用的数据反馈方法。

**Tech Stack:** Markdown、Mermaid、仓库相对链接、中文写作检查脚本、Git

---

### Task 1: 核对公开资料与内容边界

**Files:**
- Reference: `docs/plans/2026-10-13-agent-evaluation-security-design.md`
- Reference: `agent-learning-path/README.md`
- Reference: `enterprise-ai-platform/data-foundation/data-feedback-evaluation.md`

**Step 1: 核对 Agent 评测资料**

阅读用户提供的《为什么我们需要 Agent 评测》，整理任务定义、Trace、业务最终状态、新旧版本对比和回归案例维护五组观点。

**Step 2: 用一手资料校验评测方法**

查阅 Agent 评测、Trace 评测、确定性评分与模型评分的官方资料。只保留能够由公开资料或明确工程逻辑支持的结论。

**Step 3: 核对服务安全资料**

阅读 Anthropic 关于蒸馏攻击防御的官方文章，记录上下文完整性、两阶段分类、账号治理、红队测试、误报和合法用户影响。

**Step 4: 标记不写入正文的内容**

排除招聘市场热度、无法核验的大厂内部情况、作者个人稳定性数字、公司争议叙事和可直接复现的攻击提示词。

### Task 2: 调整 Agent 学习路线导航

**Files:**
- Modify: `agent-learning-path/README.md`

**Step 1: 拆分第四阶段**

将现有“工程化”拆为“可观测性与评测”和“生产治理与安全”，形成五阶段路线。

**Step 2: 增加文章入口**

在第四阶段链接 `agent-evaluation.md`，在第五阶段链接 `agent-service-security.md`。

**Step 3: 检查相对链接目标**

Run: `test -f agent-learning-path/agent-evaluation.md && test -f agent-learning-path/agent-service-security.md`

Expected: 两个文件存在，命令退出码为 0。

### Task 3: 编写 Agent 评测文章

**Files:**
- Create: `agent-learning-path/agent-evaluation.md`

**Step 1: 写清任务级评测对象**

使用订单取消示例区分回复文本、工具调用、Trace 和业务最终状态。说明 Agent 评测围绕任务、条件和完成标准展开。

**Step 2: 写入评测案例结构**

列出任务输入、初始业务状态、上下文、允许与禁止行为、预期结果、评分方法、运行版本和重复次数。

**Step 3: 写入新旧版本对比流程**

加入 Mermaid 流程图，覆盖线上反馈、问题定位、案例固化、环境恢复、重复运行、差异检查和发布门禁。

**Step 4: 解释评分责任**

确定性业务结果优先使用代码检查。语义质量可以使用人工或经过校准的模型评分。Trace 用于诊断，不能替代业务结果验收。

**Step 5: 说明评测集治理**

区分调优案例、固定回归集和未参与调优的独立评测集，并链接通用数据反馈文章。

**Step 6: 运行写作检查**

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py agent-learning-path/agent-evaluation.md`

Expected: 硬停词、模型路标、翻案腔和黑话为 0，人工判断项经过复核。

### Task 4: 编写 Agent 服务安全文章

**Files:**
- Create: `agent-learning-path/agent-service-security.md`

**Step 1: 定义威胁边界**

区分合法模型蒸馏、未授权能力提取、普通爬取和业务滥用，并说明基础模型服务商与 Agent 应用开发者的责任不同。

**Step 2: 列出 Agent 资产**

说明系统提示词、Skill、知识内容、工具描述、内部状态、受限数据和业务操作能力各自需要怎样的访问边界。

**Step 3: 设计分层防御流程**

加入 Mermaid 流程图，覆盖身份与权限、上下文完整性、请求级检测、账号与组织级聚合、渐进式处置、审计与反馈。

**Step 4: 写清检测与处置分工**

实时分类器处理单次高风险请求，长期行为聚合发现低频和跨账号协同行为。处置按观察、限流、加强验证、阻断和封禁递进。

**Step 5: 写入评测和运营指标**

覆盖攻击检测、正常流量误报、发现时间、异常调用产出、延迟、成本、合法用户影响和申诉恢复，并链接 Agent 评测文章。

**Step 6: 运行写作检查**

Run: `python3 /Users/lizhe/.codex/skills/human-writing/scripts/check_prose.py agent-learning-path/agent-service-security.md`

Expected: 硬停词、模型路标、翻案腔和黑话为 0，人工判断项经过复核。

### Task 5: 验证导航、图表和仓库状态

**Files:**
- Verify: `agent-learning-path/README.md`
- Verify: `agent-learning-path/agent-evaluation.md`
- Verify: `agent-learning-path/agent-service-security.md`

**Step 1: 检查 Markdown 差异**

Run: `git diff --check`

Expected: 没有空白错误。

**Step 2: 检查 Mermaid 围栏**

Run: `rg -n '^```mermaid|^```$' agent-learning-path/agent-evaluation.md agent-learning-path/agent-service-security.md`

Expected: 每篇文章各有一组完整的 Mermaid 围栏。

**Step 3: 检查相对链接目标**

确认两篇文章互相链接，导航链接存在，数据反馈文章目标存在。

**Step 4: 检查脱敏内容**

Run: `rg -n '客户名称|内部地址|真实账号|真实业务数据|公司内部' agent-learning-path/agent-evaluation.md agent-learning-path/agent-service-security.md`

Expected: 不出现需要脱敏的项目内容。

**Step 5: 检查最终状态**

Run: `git status --short`

Expected: 仅包含计划内的 Markdown 文件和用户原有的未跟踪 `.idea/`。

### Task 6: 保存文章提交

**Files:**
- Add: `agent-learning-path/README.md`
- Add: `agent-learning-path/agent-evaluation.md`
- Add: `agent-learning-path/agent-service-security.md`
- Add: `docs/plans/2026-10-13-agent-evaluation-security-implementation.md`

**Step 1: 暂存计划内文件**

Run: `git add agent-learning-path/README.md agent-learning-path/agent-evaluation.md agent-learning-path/agent-service-security.md docs/plans/2026-10-13-agent-evaluation-security-implementation.md`

Expected: `.idea/` 不在暂存区。

**Step 2: 检查暂存内容**

Run: `git diff --cached --check && git diff --cached --stat`

Expected: 只显示四个计划内文件，检查退出码为 0。

**Step 3: 提交**

Run: `git commit -m "docs: add agent evaluation and service security guides"`

Expected: 在 `docs/ai-education-scenarios` 分支产生一个文档提交，不推送远端。
