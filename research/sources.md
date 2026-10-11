# 来源账本

核对日期：2026-10-11。正文使用原创叙述；这里记录背景与机制来源，未镜像源站正文或媒体。

| 来源 | 使用位置 | 支持范围 | 不支持的推断 |
|---|---|---|---|
| [Palantir FDE 岗位介绍](https://jobs.lever.co/palantir/5168e8fd-fec1-4fea-b7a1-81bdaea65850) | 01 | 深入客户场景、工程交付、端到端责任 | 不能据此认定所有组织采用同一流程 |
| [启焰师道公开主页](https://teacheronhand.com/) | 前言、背景 | 教师工作流程、教学经验整理这一公开产品方向 | 不证明作者实现了网页全部功能 |
| [教师 FDE 页面](https://teacheronhand.com/fde) | 背景 | 检索可见页面摘要的教师培养主题 | 直接抓取失败；不援引不可见部分 |
| [启焰公开官网](https://www.qiyan.tech/) | 背景 | 企业和教育两类公开服务方向 | 不能推出内部架构或客户实施效果 |
| [师大网校 App 页面](https://www.sdshengben.net/app) | 背景 | 在线课堂、题库、答疑、教学等公开模块 | AI 拍搜、AI 批改的作者经历来自用户自述，不是这个网页的实现证据 |
| [李博杰 AI Infra 书稿](https://github.com/bojieli/ai-infra-book) | 仓库组织参考 | 正文、配套实验、案例和来源的组织方式 | 不复制正文、图或书名包装 |
| [Ollama chat API](https://docs.ollama.com/api/chat) | 04、06、08、示例 | /api/chat 请求与返回字段 | 未实际调用模型，不能报告生成质量 |
| [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs) | 06、示例 | 本地接口的 JSON/schema 输出约束；仍需应用验证 | 输出结构不能证明内容正确；云端支持范围需单独检查 |
| [Ollama vision](https://docs.ollama.com/capabilities/vision) | 05、示例 | 图像消息输入方法 | 不证明任何具体模型识别数学手写的准确率 |
| [LangChain retrieval](https://docs.langchain.com/oss/python/deepagents/retrieval) | 04、07 | 检索与生成组合、不同 RAG 结构 | 不保证引用存在就代表回答忠实 |
| [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | 03、06、08 | 可暂停并恢复的人工介入机制 | 样例状态函数不是生产级持久化系统 |
| [PaddleOCR 官方文档](https://www.paddleocr.ai/main/en/index.html) | 05 | OCR 与文档处理的可选工具 | 本仓库未部署 OCR 模型 |
| [Ragas Faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) | 07 | 主张与检索上下文的支持关系 | 不衡量全部数学或教学质量 |
| [Ragas Context Recall](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/) | 07 | 一种基于参考内容的召回评价 | 分母和定义不同的指标不能混用 |
| [SQS 至少一次投递](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html) | 08 | 标准队列可能重复投递，应用需幂等处理 | 本仓库没有部署 SQS 或队列 |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | 08 | 角色与持续风险管理的组织背景 | 不是本书获得认证或实际运行效果的证据 |

本地资料仅作私人写作线索，未作为公开书稿附件分发。包括教育工具构思、培训产品设计、RAG、Agent、LLM 工程化笔记。具体来源映射不纳入 Git；包含签名参数的内部图片链接未访问。笔记中的未核验性能数字未用于书稿。

独立章节的更多一手来源见 [教师案例](teacher-sources.md)、[答疑与拍搜](qa-photo-sources.md)、[批改案例](grading-sources.md)。
