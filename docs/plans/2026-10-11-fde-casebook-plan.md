# FDE Casebook Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 完成可审阅的教育案例卷及可复现的配套演示。

**Architecture:** Markdown 为正文源；单章、合订稿共享同一份正文。公共方法和五类教育案例相连，Python 演示用虚构课程与合成数据，模型接口与业务验证分开。

**Tech Stack:** Markdown、Mermaid、Python 3 标准库、unittest、可选本地 Ollama。

---

### Task 1: 素材和设计
- 读取公开网站、筛选本地 notes；不读取密钥目录，不访问内部图片链接。
- 建立 `research/sources.md`、`research/editorial-policy.md` 与设计记录；公开资料、工程建议、演示结果分开标记。

### Task 2: 并行整理独立案例章节
- 主任务编写 00、01、07、08、09。
- 独立作者编写 02、03（名师和教学流程）、04、05（答疑和拍搜）、06（批改）。仅写各自文件；来源使用一手公开资料；主任务统一审阅。
- 每章完成后检查问题→机制→实例→失败→评测理解链并向用户报告。

### Task 3: 先验证配套示例的业务约束
- 先创建 `tests/test_education.py`：课程隔离、未发布资料排除、引用伪造拒绝、低质量转写请求确认、评分证据与范围、人工发布门槛、重复发布、模型输出类型校验。
- 运行 `python3 -m unittest discover -s tests -v`，确认缺失实现失败。
- 创建 `examples/education/core.py`、`run.py`、合成 JSON。检索基线采用字符二元组，明确非向量检索；离线检查和真实模型调用分别标注。
- 重跑测试和三个 CLI，记录实际输出。未调用模型时不得报告真实模型效果。

### Task 4: 书稿与复用模板
- 创建 README、案例规格、教师访谈、量规、评测、交付模板以及未来主页入口文字。
- `scripts/build_book.py` 合并为 `BOOK.md`；生成本地阅读版本。

### Task 5: 审阅和交付
- 核对术语、数学、案例字段、命令、所有相对链接；检查图与正文的一致性。
- 检查发布文件中无内部 URL、真实凭据、个人本地路径与未核验效果数字。
- 在非保护分支提交，交付本地稿和验证记录，不自动推送或合并。
