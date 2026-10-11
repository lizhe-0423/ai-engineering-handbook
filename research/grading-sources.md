# 第 6 章来源与写作核对

核对日期：2026-10-11。章节、量规、学生作答、JSON 对象和练习均为原创合成设计；公开文献仅支持机制与限制，不支持作者经历、客户效果或公司实现的推断。未读取私人笔记、真实学生资料或公司提示词。

## 一手来源与支持边界

| 来源 | 已核对内容 | 正文使用 | 不作的推断 |
|---|---|---|---|
| [Ollama Structured Outputs](https://docs.ollama.com/capabilities/structured-outputs) | 官方文档的 Generating structured JSON with a schema；传入 `format`，示例随后以 Pydantic 或 Zod 解析/验证 | 结构化输出提供后端契约，应用仍执行字段、范围和证据检查 | Schema 符合不意味着数学、量规或反馈正确；不宣称已调用某一模型 |
| [Zheng et al. (2023), Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) | 原论文摘要列出 position、verbosity、self-enhancement bias 和 limited reasoning ability；研究任务是聊天回答评判 | 说明模型评判存在偏好和推理边界，需要单独评测教育评分 | 不把论文对聊天偏好的协议或结果移植成数学作业准确率；正文不使用性能数字 |
| [Hwang et al. (2025), Can You Trick the Grader? Adversarial Persuasion of LLM Judges](https://aclanthology.org/2025.findings-emnlp.790/) | ACL 原论文摘要：数学推理评分中，在内容相同的解答里加入说服策略会影响评分；明确研究了错误答案的分数膨胀 | 提出在合成评测中加入求情、权威或请求满分等与数学无关的文本 | 不声称所有模型或本地模型都有相同程度的偏差；不复用论文攻击语料或效果数字 |
| [LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | Pause using interrupt、Resuming interrupts、Side effects called before interrupt must be idempotent；恢复会从节点起点重跑，需要 checkpointer 与一致的 thread ID | 解释等待人工决定、持久化状态、重跑及幂等副作用 | 不声称本书 CLI 已部署 LangGraph、数据库、队列或生产持久化；不把框架中断当作身份权限校验 |
| [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf) | MAP 3.5：人工监督流程需要定义、评估和记录；附录 C 讨论人类角色与决策责任 | 教师审核流程要有具体责任与记录，而不只是 UI 上一个确认按钮 | 框架为通用风险管理资料，不是教育评分法律意见，也不强制所有任务采用同一审核策略 |

## 推导与原创内容

本文“C1=2、C2=1、C3=0”的部分分数直接来自原创量规，不来自文献测量。错误草稿把 `x=2` 对应的 C2 判为 2 分，是为了说明原文引用存在与评分依据充分之间的差别，没有冒充真实模型记录。

量规中特意规定：本题指定因式分解，C3 须验证两个根。公式法可得到正确根，但不能自动满足指定方法的 C1。若题目不限方法，应先改成接受等价解法的量规，再对同批作答一致应用新版；这是案例的教研流程选择。

结构验证检查字段、项目唯一且完整、严格整数分数、分值范围以及证据确属学生文本。字符串 `"2"` 和布尔值不作为得分接受。此类程序验证不等于数学正确性、评分效度或教学反馈质量。

任务键、版本快照、过期结果拒绝覆盖、教师批准绑定结果版本、发布唯一键和事务门槛是原创工程设计。状态图展示目标工作流，正文明确配套 CLI 只演示校验与纯函数门槛：`validate_grade` 返回 `total:3`、`max_score:5`、`status:teacher_review`；`publish_grade` 要求明确批准和非空审核人，重复传入已发布对象返回同值。服务端鉴权、数据库事务和消息队列尚不属于本版实现，不能把目标流程写成已上线功能。

OCR 分数与模型自报信心均未按真实评分误差校准。文中不给出准确率、时延、成本、概率阈值或课堂收益。离线夹具只回放作者写好的建议并检查结构及状态；`--model MODEL` 才调用本地 Ollama，输出仍是草稿。

## 编辑与视觉检查记录

最短理解链：漏根的满分错判 → 量规与原文证据 → 可解析评分契约 → 合法对象中的语义错误 → 等价方法与 OCR → 异步版本与教师批准 → 跟做失败样本。

配图计划为一张精确状态 Mermaid 图，负责展示“校验通过只到待审核”及重复发布的结果；评分表负责逐项对照，不增加装饰图片。已按教程编辑参考检查套话、虚构经验、指标夸张、章节导航与引用支持范围。链接均直接指向一手文档或原论文。
