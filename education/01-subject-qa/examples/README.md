# 学科答疑最小示例

[阅读正文](../01-answering-pipeline.md) · [学科答疑目录](../README.md)

用三个合成案例演示已确认文本的答疑路由。Python 3.10+，仅用标准库；命令在仓库根目录运行。课程、题目、材料都写在 [`data/cases.json`](data/cases.json)，`approved` 由夹具预设，示例没有审核后台。

```bash
# 题库同题：返回固定的已审核首步提示
python3 education/01-subject-qa/examples/run.py --case math_bank

# 同题完整讲解
python3 education/01-subject-qa/examples/run.py --case math_bank --level solution

# 物理：课程资料进入 RAG 请求
python3 education/01-subject-qa/examples/run.py --case physics_rag

# 数学：没有题库同题或材料，课程允许独立生成
python3 education/01-subject-qa/examples/run.py --case math_direct

# 模拟需要用户确认的题干
python3 education/01-subject-qa/examples/run.py --case math_bank --unconfirmed
```

未指定 `--model` 时不会访问模型服务。`curated / answered` 表示题库已有讲解；`rag` 和 `direct` 的 `model_required` 表示请求已准备，`reply` 仍为空。`prepared_request` 可用于查看教师策略、题干、材料与输出结构。

## 使用本地模型

先自行启动 Ollama，并准备一个支持结构化输出的本地模型。将下面的 `YOUR_LOCAL_MODEL` 替换为 `ollama list` 中已有的模型名称：

```bash
python3 education/01-subject-qa/examples/run.py --case physics_rag --model YOUR_LOCAL_MODEL
python3 education/01-subject-qa/examples/run.py --case math_direct --level solution --model YOUR_LOCAL_MODEL
```

请求发送至 `http://localhost:11434/api/chat`，不自动下载模型、不读取云端令牌。取到模型返回后，CLI 才记录 `model_call_performed: true`。HTTP、结构或引用验证失败会返回非零退出码，在标准错误流写出原因；不会替换成固定答案。题库同题即使传了 `--model` 也不调用模型。

`validated_draft` 只表示模型结果通过字段与引文检查。数学错误、材料不支持结论、直接泄露完整答案等仍需要内容检查，输出保留 `requires_content_review: true`。因此示例适合研究与人工查看，不能直接当作面向学生的自动放行服务。

## 代码与测试

| 文件 | 作用 |
|---|---|
| [qa_core.py](qa_core.py) | 课程与审核过滤、同题匹配、词面检索、教师策略组装、引用检查 |
| [run.py](run.py) | 案例选择、默认请求准备、显式模型调用与退出码 |
| [ollama_client.py](ollama_client.py) | 本地非流式 Chat API，两层 JSON 分开解析 |
| [tests/](tests/) | 路由、隔离、冲突、假引用、默认无调用与异常响应 |

```bash
python3 -m unittest discover -s education/01-subject-qa/examples/tests -v
```

词面检索只按中文双字片段和英文/数字词元的交集排序，取最多三条有重叠的资料。它用来观察流程，没有向量模型、语义召回和经过评测的相关性阈值。课程上下文来自调用方；实际服务仍需在认证后解析课程权限，不能让用户自己填写课程标识来获得资料。

本例没有图片识别、数据库、多轮会话、工具执行或生产鉴权。数学与物理夹具可独立核算；测试验证程序边界，不能证明模型效果或教学收益。
