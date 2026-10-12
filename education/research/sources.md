# 技术来源

正文在相关讨论处直接链接原论文和官方文档，本页方便按主题查找。课程资料、例题和流程图另行编写，没有收录公司产品文案或内部材料。

| 主题 | 来源 | 用途 |
|---|---|---|
| FDE | [Palantir 岗位介绍](https://jobs.lever.co/palantir/5168e8fd-fec1-4fea-b7a1-81bdaea65850) | 第 1 章的业务理解与工程交付视角 |
| 学科教学知识 | [Shulman，1986](https://journals.sagepub.com/doi/10.3102/0013189X015002004) · [原文副本](https://home.miracosta.edu/rfrench/documents/Shulman_1986.pdf) | 第 2 章的讲解、表示方法与学生误解 |
| 自我解释 | [Chi 等，1994](https://education.asu.edu/sites/g/files/litvpz656/files/lcl/chideleeuwchiulavancher_3.pdf) | 第 2 章的学习者解释；原研究任务为循环系统材料，不作为本例数学教学效果证据 |
| 数据来源 | [W3C PROV](https://www.w3.org/TR/prov-overview/) | 来源、活动和参与者之间的关系 |
| 数据结构 | [JSON Schema object](https://json-schema.org/understanding-json-schema/reference/object) | 字段、必填与类型约束 |
| 状态转换 | [W3C SCXML](https://www.w3.org/TR/scxml/) | 状态、事件及转换条件 |
| 人工中断 | [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | 暂停、恢复和重跑中的副作用 |
| RAG | [Lewis 等，2020](https://arxiv.org/abs/2005.11401) | 检索与生成的组合思想；配套词面检索并非论文模型的复现 |
| 检索接口 | [LangChain retrieval](https://docs.langchain.com/oss/python/deepagents/retrieval) | 检索与生成的模块划分 |
| 本地模型 | [Ollama chat](https://docs.ollama.com/api/chat) · [结构化输出](https://docs.ollama.com/capabilities/structured-outputs) · [图像输入](https://docs.ollama.com/capabilities/vision) | 可选模型适配器的请求与响应 |
| OCR | [PaddleOCR](https://www.paddleocr.ai/main/en/version3.x/pipeline_usage/OCR.html) | 检测区域、文字、分数及坐标；当前示例未集成 OCR |
| 分数校准 | [Guo 等，2017](https://arxiv.org/abs/1706.04599) | 预测分数与正确频率之间的关系 |
| 检索评测 | [Ragas Context Recall](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/) · [Faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) | 参考内容覆盖、回答与上下文的支持关系 |
| 模型评价 | [MT-Bench，2023](https://arxiv.org/abs/2306.05685) | 位置、冗长等评价偏差 |
| 评分干扰 | [Can You Trick the Grader?，2025](https://aclanthology.org/2025.findings-emnlp.790/) | 与解答内容无关的说服文本对评分的影响 |
| 重复消息 | [SQS 至少一次投递](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html) | 消费和发布中的幂等处理 |
| 运行管理 | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) · [1.0 原文](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf) | 角色职责、人工监督与持续管理 |

外部文献用于解释机制，不能替代本例的实验。程序已做的检查见[验证记录](../../docs/verification.md)；后续模型实验记录数据、模型和判据后，再补充结果。
