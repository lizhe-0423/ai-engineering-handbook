# FDE 案例集

**从业务问题到 AI 应用交付 · Blueberry**

这是一份围绕真实业务问题类型编写的原创教程。它把需求、证据、模型输出、人工复核和工程交接连起来，帮助读者理解一个 AI 应用为什么这样设计，以及失败时怎样定位和接手。

**当前版本：教育卷 0.1，审阅稿。** 包含序言、9 章正文、合成案例、可运行的 Python 演示与复用模板。书中的访谈、例题、故障和作答均为原创合成材料，不是任何公司的生产系统复现。

## 阅读

从[合订稿](BOOK.md)开始，或按下面目录逐章阅读。`build/reading.html` 是本地生成的离线阅读版，流程图在构建时渲染。

| 章节 | 读完后能做什么 |
|---|---|
| [序言](chapters/00-preface.md) | 区分教育场景、FDE 交付与演示的验证范围 |
| [1 · FDE 方法](chapters/01-fde-method.md) | 把业务诉求写成有输入、证据、动作与验收的案例 |
| [2 · 教师经验](chapters/02-teacher-knowledge.md) | 用反例访谈整理教学判断及其适用条件 |
| [3 · 教学流程](chapters/03-teaching-workflow.md) | 用状态、版本与复核让备课流程可以暂停和修订 |
| [4 · 课程答疑](chapters/04-course-qa.md) | 检查课程隔离、检索材料和引用边界 |
| [5 · 拍照搜题](chapters/05-photo-search.md) | 区分转写、原题匹配和不确定符号的确认 |
| [6 · 作业批改](chapters/06-homework-grading.md) | 用量规、原文证据与审核组织评分草稿 |
| [7 · 评测](chapters/07-evaluation.md) | 在输入、证据、内容与动作四层定位失败 |
| [8 · 交付](chapters/08-delivery.md) | 设计快照、重复任务、运行记录与交接 |
| [9 · 案例复用](chapters/09-case-library.md) | 把案例变成别人能重跑、修改与检查的材料 |

开发者可以从 1→4→5→6→7→8 开始；教师和教研人员可以先读 2→3→6→7，再看工程约束。

## 十分钟运行离线演示

需要 Python 3.10 或更新版本，无需安装第三方 Python 包。在仓库根目录运行：

```bash
# 获取已审核、当前课程内的候选证据，不生成回答
python3 examples/education/run.py qa --question "二次方程怎么因式分解"

# 检查合成转写的精确题干匹配
python3 examples/education/run.py photo --fixture examples/education/data/photo-clear.json

# 模糊符号应请求确认
python3 examples/education/run.py photo --fixture examples/education/data/photo-uncertain.json

# 检查预先编写的分项评分：3/5，仍待教师复核
python3 examples/education/run.py grade --fixture examples/education/data/grade-partial.json

python3 -m unittest discover -s tests -v
python3 scripts/check_book.py
```

| 默认模式 | 实际运行内容 | 不能据此得出的结论 |
|---|---|---|
| `offline_evidence` | 词面检索、课程和审核状态过滤 | 答疑正确率、语义检索效果 |
| `synthetic_transcription_route` | 固定转写、确认路由、精确文本匹配 | 图像或手写识别准确率 |
| `synthetic_grade_validation` | 固定建议的类型、证据、范围与求和 | 模型批改准确率、教学效果 |

拍搜的 `exact_match` 是候选匹配，仍带 `requires_visual_confirmation: true`；批改结果停在 `teacher_review`。程序约束通过不等于解释或分数符合教学要求。

## 可选：接入自己的本地模型

先自行准备并启动 [Ollama](https://docs.ollama.com/)，安装所需模型。以下 `MODEL` 替换为已有模型名，`VISION_MODEL` 须支持图片。代码只调用本机 `localhost:11434`，不会自动下载模型。

```bash
python3 examples/education/run.py qa --question "二次方程怎么因式分解" --model MODEL
python3 examples/education/run.py photo --image your-question.png --model VISION_MODEL
python3 examples/education/run.py grade --fixture examples/education/data/grade-partial.json --model MODEL
```

这些入口使用 JSON Schema 和业务检查接收草稿。本次交付没有运行真实模型，没有课堂实验；模型名称、数据版本、原始输出和内容评阅需要填入[评测记录](templates/evaluation-record.md)。服务端鉴权、持久化任务、队列及审核界面属于第 8 章的进一步交付设计。

## 复用与维护

- [案例规格](templates/case-spec.md)：确定任务与失败动作。
- [教师访谈](templates/teacher-interview.md)：保留判断证据与适用条件。
- [评分量规](templates/grading-rubric.md)：明确过程分、等价方法与缺失证据。
- [评测记录](templates/evaluation-record.md)：记录运行条件及实际结果。
- [交付检查单](templates/delivery-checklist.md)：验证接手人能运行、复核与恢复。
- [来源与引用说明](research/sources.md)、[编辑约定](research/editorial-policy.md)、[验证记录](docs/verification.md)。

编辑 `chapters/` 后运行 `python3 scripts/build_book.py` 重新生成合订稿。[本地阅读构建说明](docs/build-reading.md)说明怎样把流程图渲染进 HTML。

后续卷计划覆盖企业知识库与物联网应用，待完成具体案例后加入。当前先维护教育卷，不把规划当成已有成果。

## 作者

[Blueberry](https://github.com/lizhe-0423) · AI Agent Engineer · [掘金](https://juejin.cn/user/1420997038194350)

正文与代码为原创审阅稿；公开引用保留原来源。公开再分发许可证尚未确定；外部资料各自适用原许可。
