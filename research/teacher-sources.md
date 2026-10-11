# 教师经验与教学工作流：来源与核对记录

核对日期：2026-10-11。对应第 2、3 章。正文为原创教程初稿，待作者核对经历背景及可公开范围。没有复制公司培训框架、话术、内部架构或生产数据；没有读取私人 notes、飞书下载链接或公司图片。

## 一手来源

| 来源 | 实际查阅与支持范围 | 章节中的使用 | 不支持的推断 |
|---|---|---|---|
| [启焰师道公开主页](https://teacheronhand.com/) | 核对公开页面把教师工作流程、教师审核及经验整理列为产品方向，以及 S7 名称的出现 | 02 开篇背景；03 术语边界 | 不能证明 Blueberry 参与网页全部功能，不能证明客户效果，也不能把教师 FDE 或 S7 写成行业通用标准 |
| [Shulman，Those Who Understand: Knowledge Growth in Teaching，1986](https://journals.sagepub.com/doi/10.3102/0013189X015002004) | 原论文区分学科内容、学科教学与课程知识；学科教学知识讨论表示方法、解释及学生误解。出版页只显示元数据，另读了[公开原文副本](https://home.miracosta.edu/rfrench/documents/Shulman_1986.pdf)，重点核对论文第 9 页对应段落 | 02 解释采集对象为何包含教学判断 | 不能证明 AI 技能卡、数字形象或本案例具有已验证教学效果 |
| [W3C PROV Overview](https://www.w3.org/TR/prov-overview/) | provenance 描述产生数据或事物的实体、活动和参与者关系 | 02 来源关联与版本追踪的概念背景 | 本书卡片未实现完整 PROV 标准，追踪信息不自动证明内容可靠 |
| [Chi 等，Eliciting Self-Explanations Improves Understanding，1994 原论文](https://education.asu.edu/sites/g/files/litvpz656/files/lcl/chideleeuwchiulavancher_3.pdf) | 阅读循环系统说明材料的自我解释实验；核对原论文摘要及任务范围 | 02 要求学习者解释理由的研究背景，正文保留任务边界 | 不能外推为二次方程技能卡或 AI 教学效果；未转写实验数字作产品收益 |
| [JSON Schema：object](https://json-schema.org/understanding-json-schema/reference/object) | 属性声明、必填字段、额外字段；属性不会自动成为必填字段 | 03 输入输出的类型约束 | JSON 合法或符合 schema 不等于数学正确、教学合适或审批有效 |
| [W3C SCXML](https://www.w3.org/TR/scxml/) | 状态、事件及带条件的转换；核对概览与 3.5 节 | 03 有条件地进入可用状态 | Mermaid 图没有实现 SCXML 运行时或生产持久化 |
| [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | 暂停与恢复需要保存状态及任务标识；恢复会重跑所在节点，中断前副作用需要考虑幂等 | 03 人工介入、恢复及重复发布边界 | 本章没有部署 LangGraph；图示或单一发布键本身不能证明生产系统无重复写入 |

`https://teacheronhand.com/fde` 的直接网页抓取失败，本稿不引用它的不可见内容。公司语境只使用已打开首页能够核对的最小事实。未访问其白皮书、付费课程或内部资源。

## 原创设计与实际检查

- 02 的访谈、作答、`zero-product-explain@0.1` 卡片、两次补充后交教师的停止规则均为原创合成示例。“两次”是演示约定，未经教育效果验证。
- 03 的时间表是 20 分钟备课演练预算，不是课堂统一时长，也不是节省备课时间的实测结论。三问、状态图、输入类型表和 SOP 重新设计。
- 03 的失败样本由作者人为构造，用于回放“旧审核放行新草稿”的确定性漏洞，没有声称它发生在真实公司项目中。
- 2026-10-11 用 Python 解析正文 JSON 并检查：旧条件 `decision == approve` 返回 True；审核版本 1 不匹配草稿版本 2；错误根 0、5 代入 `x²-5x+6` 的残差均为 6。合法根 2、3 的残差均为 0。这些检查证明反例和数学关系，不证明模型质量或学习效果。
- 逐章含一个 Mermaid 源图；02 为来源到调用的流程，03 为可暂停状态。图的节点、条件与正文逐项核对，保留可编辑源码。

## 作者复核事项

本稿不增加 Blueberry 的第一人称亲历。需要作者确认背景表述是否符合实际参与范围；需要教师确认访谈示例、追问顺序、前置条件和转人工规则是否适合拟定课程。实际模型输出、教师使用体验和学习变化需以后另行采样，不能从合成回放推定。
