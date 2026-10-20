# 企业级 AI 生产平台

[← 返回首页](../README.md)

企业把 AI 做进日常业务，需要一套能够长期运行的生产体系。数据要持续进入，模型要经过评测和部署，知识内容需要维护，最终能力还要接入真实业务流程。

这套体系可以拆成四个相互连接的部分。

| 工程领域 | 处理的问题 |
|---|---|
| [数据工程与智能标注](data-foundation/README.md) | 数据接入、清洗、标注、质量检查与版本管理 |
| [模型工程与服务治理](model-engineering/README.md) | 训练、评测、部署、推理服务与运行管理 |
| [知识工程与内容生产](knowledge-engineering/README.md) | 知识整理、检索、内容生成、质量评估与人工审核 |
| [智能体服务与业务编排](agent-applications/README.md) | 企业问答、任务分流、工作流执行、人工接管与系统集成 |

四个部分可以独立建设，也可以组成完整链路。平台设计需要先解决数据和责任边界，再考虑模型能力与交互形式。

具体业务可以从[复杂文档解析与转换](knowledge-engineering/document-conversion.md)和[岗位带教 Agent](agent-applications/workplace-coaching-agent.md)开始看，分别说明资料怎样加工成可靠输入，以及方法怎样进入可复核的任务流程。
