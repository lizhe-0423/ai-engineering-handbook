# 教育 AI 应用实践

[← 总目录](../README.md)

这里讨论教师知识整理、课程答疑、拍照搜题和作业批改。贯穿例题是 `x²-5x+6=0`，让读者可以手动核对答案，再看资料、模型和业务流程怎样衔接。

## 目录

| 章节 | 主要问题 |
|---|---|
| [前言](chapters/00-preface.md) | 答疑、拍搜和批改为什么要分开设计 |
| [1 · 需求与验收](chapters/01-fde-method.md) | “回答正确”怎样变成可检查的条件 |
| [2 · 教师经验](chapters/02-teacher-knowledge.md) | 如何记录讲解、追问和判断条件 |
| [3 · 教学流程](chapters/03-teaching-workflow.md) | 草稿、修订和审核怎样保持一致 |
| [4 · 课程答疑](chapters/04-course-qa.md) | 资料过滤、检索与引用各负责什么 |
| [5 · 拍照搜题](chapters/05-photo-search.md) | 原图、转写和候选题如何核对 |
| [6 · 作业批改](chapters/06-homework-grading.md) | 评分规则、作答证据与复核怎样衔接 |
| [7 · 评测](chapters/07-evaluation.md) | 怎样定位输入、证据、内容和动作的错误 |
| [8 · 服务交付](chapters/08-delivery.md) | 重复任务、补交作答和旧结果怎样处理 |
| [9 · 案例维护](chapters/09-case-library.md) | 改一道题时，哪些材料要一起修改 |

[连续阅读合订稿](BOOK.md)。开发者可以先看 4→5→6，再读评测与交付；关注教学经验和备课，可以先看 2→3。

## 运行示例

需要 Python 3.10 或更新版本，没有第三方 Python 依赖。下面命令都在**仓库根目录**运行。

```bash
# 获取当前课程内的已审核证据
python3 education/examples/run.py qa --question "二次方程怎么因式分解"

# 匹配清晰转写，返回待核对的候选题
python3 education/examples/run.py photo --fixture education/examples/data/photo-clear.json

# 符号不确定时请求确认
python3 education/examples/run.py photo --fixture education/examples/data/photo-uncertain.json

# 检查评分建议，返回 3/5 分的待复核草稿
python3 education/examples/run.py grade --fixture education/examples/data/grade-partial.json
```

课程资料、题目、学生作答和测试输出均为重新编写的合成数据。默认运行不会调用模型：答疑做词面检索，拍搜处理预先给定的转写，批改检查预先编写的评分建议。

`exact_match` 仍带 `requires_visual_confirmation: true`，需要核对原图；评分停在 `teacher_review`。这些检查验证程序约束，不代表模型答疑、图片识别或教学效果已经实测。

### 可选：本地模型

准备并启动 [Ollama](https://docs.ollama.com/)，把 `MODEL` 换成已安装的模型名；`VISION_MODEL` 需要支持图片。代码请求本机 `localhost:11434`，不会自动下载模型。

```bash
python3 education/examples/run.py qa --question "二次方程怎么因式分解" --model MODEL
python3 education/examples/run.py photo --image your-question.png --model VISION_MODEL
python3 education/examples/run.py grade --fixture education/examples/data/grade-partial.json --model MODEL
```

模型输出仍经过业务检查，并保留为待评阅结果。本版未运行模型或课堂实验；如果自行实验，请保存输入、配置和原始输出，填写[评测记录](templates/evaluation-record.md)。第 8 章的鉴权、数据库、队列与审核页面属于服务扩展设计。

## 表单与维护

| 用途 | 文件 |
|---|---|
| 明确任务与失败动作 | [案例规格](templates/case-spec.md) |
| 记录讲解及适用条件 | [教师访谈](templates/teacher-interview.md) |
| 确定过程分与解法要求 | [评分量规](templates/grading-rubric.md) |
| 保存实验条件和输出 | [评测记录](templates/evaluation-record.md) |
| 核对接手与恢复步骤 | [交付检查单](templates/delivery-checklist.md) |

修改单章后，在仓库根目录重新生成合订稿并检查：

```bash
python3 scripts/build_book.py
python3 scripts/check_book.py
python3 -m unittest discover -s education/tests -v
```

[本地 HTML 阅读版](../docs/build-reading.md) · [验证记录](../docs/verification.md) · [技术来源](research/sources.md) · [编辑约定](research/editorial-policy.md)
