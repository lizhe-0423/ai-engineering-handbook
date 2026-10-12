# 教育篇验证记录

## 2026-10-12：学科答疑首篇

新增正文 `education/01-subject-qa/01-answering-pipeline.md`，独立示例位于相邻 `examples/`。首页按三个阅读方向组织，细分选题记录在 `education/research/topic-map.md`。

| 检查 | 结果 |
|---|---|
| `python3 -m unittest discover -s education/01-subject-qa/examples/tests -v` | 26 项通过：同题、冲突、课程与审核过滤、生成权限、引用、默认无调用、模型响应结构、数据及 HTTP 失败 |
| `python3 -m unittest discover -s education/tests -v` | 原示例 27 项通过 |
| 三个新案例的默认 CLI | `curated / answered`、`rag / model_required`、`direct / model_required`，均记录 `model_call_performed: false` |
| 额外 CLI | `solution` 返回已审核完整解法；`--unconfirmed` 请求确认题干 |
| `python3 scripts/check_book.py` | Markdown 本地链接、围栏、JSON 和旧稿锚点检查无问题；JSON 夹具扩大到整个教育目录 |
| 新正文图示与预览 | 2 张 Mermaid 渲染无错误，桌面图示完整可见；手机正文无横向溢出，宽图在图内滚动 |
| 独立审阅 | 课程边界与正文契约一致；补充了数据文件损坏、HTTP 响应中断的统一错误处理，并用回归测试核对 |

测试中的模型响应由测试夹具提供；这些测试不证明实际生成质量。本机 Ollama 的只读模型列表请求在 2 秒内未返回，本次没有运行真实模型。结构与引文检查通过的结果仍标为 `validated_draft`、`requires_content_review: true`，不自动放行给学生。

例题可核算：不等式解为 `x>2`；匀速运动中 `72 km/h = 20 m/s`，10 s 的路程为 200 m；圆面积为 `9π cm²`。检索示例是词面基线，没有 OCR、向量召回、数据库或生产认证，也没有教学收益结论。

## 2026-10-11：上一版目录与正文

日期：2026-10-11。本次调整了总目录、教育子目录和全部正文，配套算法行为保持原样。

## 本地检查

| 操作 | 结果 |
|---|---|
| `python3 -m unittest discover -s education/tests -v` | 27 项通过，覆盖课程过滤、引用、转写路由、评分约束、发布纯函数和离线 CLI |
| 答疑离线示例 | `offline_evidence`，返回当前课程两条已审核证据，不生成答案 |
| 清晰转写示例 | `exact_match`，保留 `requires_visual_confirmation: true` |
| 模糊符号示例 | `ask_confirmation` |
| 评分示例 | `total: 3`、`max_score: 5`、`status: teacher_review` |

CLI 统一由 `python3 education/examples/run.py` 启动。原始资料、作答和建议使用合成数据；本次没有运行真实模型、OCR 或课堂实验，因此没有识别准确率、评分准确率和教学收益结论。

## 正文与目录

单章、合订稿和文档链接由构建检查统一核对。原来的产品名称、品牌框架、产品网址及背景引用从本次修订的文件中移除；技术来源保留原论文和官方文档。

正文中的数学可以独立检查：2、3 代回 `x²-5x+6` 为零，0、5 的结果为 6。漏根并未验证的作答，按示例量规为 3/5 分。

队列、鉴权、数据库、版本批准和事务发布是服务扩展设计。现有纯函数不包含这些能力；教师改分后需要重新检查分项并计算总分。

构建结果：10 份正文生成教育合订稿；26 份 Markdown、5 份 JSON 夹具、本地链接、围栏及章节锚点检查无问题。9 张 Mermaid 图全部渲染，桌面与手机截图已查看。HTML 本地链接无缺失，导出页无运行时脚本。
