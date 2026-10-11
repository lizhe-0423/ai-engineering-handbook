# AI 应用工程案例集

**Blueberry · 从业务问题到工程实现**

我把 AI 应用开发中的问题按业务领域整理在这里：需求怎样拆，资料怎样组织，模型结果怎样检查，服务出错后怎样处理。先从熟悉的教育场景开始，逐步补充其他领域。

## 案例目录

| 领域 | 内容 | 阅读入口 |
|---|---|---|
| 📚 教育 | 教师经验整理、备课流程、课程答疑、拍照搜题、作业批改，以及评测和交付 | [进入教育目录 →](education/README.md) |

教育篇包含 9 章正文、配套 Python 示例、测试数据和表单。想连续阅读，可以打开[教育合订稿](education/BOOK.md)；想先看一个具体功能，可以从[答疑](education/chapters/04-course-qa.md)、[拍搜](education/chapters/05-photo-search.md)或[批改](education/chapters/06-homework-grading.md)开始。

## 目录结构

```text
.
├── README.md                 总目录
├── education/                教育
│   ├── README.md             教育目录与运行说明
│   ├── chapters/             文章
│   ├── examples/             示例代码与数据
│   ├── tests/                程序检查
│   ├── templates/            案例、量规与交付表单
│   ├── research/             引用说明
│   └── BOOK.md               教育合订稿
├── scripts/                  构建与文档检查
└── docs/                     维护说明与验证记录
```

新领域完成具体案例后，再作为独立目录加入这里。[维护说明](education/chapters/09-case-library.md)介绍怎样让正文、规则、数据和代码保持一致。

---

[Blueberry](https://github.com/lizhe-0423) · AI Agent Engineer · [掘金](https://juejin.cn/user/1420997038194350)
