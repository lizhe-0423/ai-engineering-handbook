# 案例集重排与编辑计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 建立按领域进入的总案例目录，完整改写教育文章并移除前雇主相关材料。

**Architecture:** 根 README 只保留总介绍和领域入口。教育正文、示例、模板、来源和测试统一放入 `education/`；根 `scripts/` 构建教育合订稿与阅读页。

**Tech Stack:** Markdown、Mermaid、Python 标准库、现有 Node 阅读页构建器。

## 1. 目录与运行路径

移动教育文件，更新测试、构建脚本和文内链接。运行 `python3 -m unittest discover -s education/tests -v`，应通过现有 27 项测试。

## 2. 逐章编辑

独立编辑教师知识与流程（02–03）、答疑与拍搜（04–05）、作业批改（06）。主任务编辑前言、需求规格、评测、交付与案例维护（00–01、07–09），并统一审阅。保留技术机制、代码行为和事实限制，删除套话与重复预告，不编造作者亲历。

## 3. 来源与命名

只保留正文实际使用的技术论文及官方文档。检查全文和辅助文档中的前雇主标识与链接。README 使用《AI 应用工程案例集》，仓库 About 简介记录为“围绕实际业务问题，整理 AI 应用的设计思路、工程实现与交付经验。”

## 4. 验证与发布

生成 `education/BOOK.md`，检查本地链接、JSON、章节和图。运行离线示例及 27 项测试，渲染桌面与手机阅读页。检查最新远程 main 后将文档分支变基，发布一个工作提交并创建新 PR；不合并 PR、不写 main。
