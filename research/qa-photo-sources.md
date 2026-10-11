# 课程答疑与拍照搜题来源记录

核对日期：2026-10-11。正文位置：`chapters/04-course-qa.md` 与 `chapters/05-photo-search.md`。两章数学、课程资料、数据规格、流程图及练习均为原创合成案例，没有引用实际学校、学生、客户或生产效果。

## 一手资料及可支持的事实

| 来源 | 可支持的事实 | 正文使用边界 |
|---|---|---|
| [Lewis 等：Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)，2020 | 原始 RAG 研究组合参数化生成模型与可检索的非参数外部记忆；论文系统使用密集检索 | 解释 RAG 思想，不声称本书字符二元组基线复现论文实现，不移用论文效果数字 |
| [LangChain：Retrieval](https://docs.langchain.com/oss/python/deepagents/retrieval) | 检索器根据查询返回文档，检索可独立于生成；两步 RAG 先检索后生成 | 解释模块边界；演示是 Python 标准库，不依赖 LangChain |
| [Ollama：Structured Outputs](https://docs.ollama.com/capabilities/structured-outputs) | `format` 可接收 JSON Schema；输出仍可使用外部验证器检查 | 仅支持结构化接口选择；不能由 JSON 合法推导数学或教学正确 |
| [Ollama：Vision](https://docs.ollama.com/capabilities/vision) | 视觉模型可接收图片与文本；REST API 通过消息 `images` 发送 base64 图片数据 | 支持显式启用的本地图像转写路径；没有运行模型或报告识别效果 |
| [Ollama：Generate a chat message](https://docs.ollama.com/api/chat) | 聊天生成入口为 `POST /api/chat`，请求提供模型与消息列表 | 用于核对父任务可选适配器，正文没有复制官方代码示例 |
| [PaddleOCR：General OCR Pipeline Usage Tutorial](https://www.paddleocr.ai/main/en/version3.x/pipeline_usage/OCR.html) | 通用 OCR 输出包含识别文本、识别分数与区域坐标，文档区分检测和识别 | 用于说明区域溯源；本版没有集成 PaddleOCR，也没有推断普通文字 OCR 能正确读取全部数学结构 |
| [Guo 等：On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599)，2017 | 校准讨论预测分数与实际正确频率的一致关系 | 提供校准定义；不是对本书所用模型的实测，也不声称论文证明所有 VLM 自报分数的具体误差 |

旧链接的重定向已核对：LangChain 的 `/oss/python/langchain/retrieval` 当前转到 `/oss/python/deepagents/retrieval`；PaddleOCR 的 GitHub Pages OCR 使用文档转到 `www.paddleocr.ai`。正文使用最终可访问的官方链接。动态文档日后可能变化，应在适配器升级时重新核对。

## 本书工程设计与文献事实分开记录

课程过滤、只使用 `status="approved"` 的材料、保留片段版本、逐项检查引文、把证据缺口转交教师，是本书的演示规则与工程建议。文献不会替本书证明这些规则适用于所有课程。

拍照流程中的完整裁切、关键符号确认、原题与相似题分开展示、转写版本绑定匹配结果，是本书原创产品设计。只有图片、人工标准转写与实际运行输出才能验证具体识别系统；合成夹具不能提供此项证据。

## 与配套实现的契约

- 文档字段：`id`、`course_id`、`status`、`text`、`title`、`version`。检索先限定课程与审核状态，返回值带 `lexical_overlap`。词面特征包括字符二元组及字母数字词项，重合率不是概率；未使用语义向量。
- QA 默认只输出证据；显式 `--model MODEL` 激活 Ollama。模型答疑契约为 `answer: str`、`next_action: answer | teacher_review`、`citations: [{document_id, quote}]`。结构、ID、课程、审核状态与字面引用检查不能证明推理忠实。
- 拍照夹具字段：`text`、`uncertain_regions: list[str]`、`provenance: synthetic_transcription_fixture`。它直接提供转写，没有调用 OCR/VLM。存在任何不确定区域即请求确认。
- 拍照基线仅归一化空白、`²` 和 Unicode 减号，再进行精确文本匹配；保留正负与条件。路由为 `ask_confirmation`、`exact_match`、`teacher_review`。相似题召回与 rerank 属于章节中讨论的扩展设计，未称为实现功能。
- 实际图像入口需要用户图片、显式模型名称、本地服务与视觉模型准备完成；“模型没有报不确定”不等于图片读取正确。

## 作者已做与仍需主任务验证的工作

作者已核对一手来源，检查例题分解与两个根，核对示例字段、CLI 入口、图中文字与正文的模式边界，并完成教程感编辑。未开展 OCR/VLM 实测，没有准确率、延迟或教学效果数字。Mermaid 图与章节链接由合订稿构建及最终渲染统一检查。
