# AI 应用工程案例集

**Blueberry · 从业务问题到工程实现**

我把 AI 应用开发中的问题按业务领域整理在这里：需求怎样拆，资料怎样组织，模型结果怎样检查，服务出错后怎样处理。先从熟悉的教育场景开始，逐步补充其他领域。

## 案例目录

| 领域 | 内容 | 阅读入口 |
|---|---|---|
| 📚 教育 | 序章、学科答疑、智能批改、AI 视频教学、数字名师、个性化学习、成长陪伴与 AI 智慧课堂 | [进入教育目录 →](education/README.md) |

教育部分从[序章](education/00-preface/README.md)开始。学科答疑已经整理出一篇[完整教程](education/01-subject-qa/01-answering-pipeline.md)，并附有[可运行示例](education/01-subject-qa/examples/README.md)。

## 目录结构

```text
.
├── README.md                 总目录
├── education/                教育
│   ├── 00-preface/           序章
│   ├── 01-subject-qa/        学科答疑
│   ├── 02-grading/           智能批改
│   ├── 03-video-teaching/    AI 视频教学
│   ├── 04-digital-teacher/   数字名师
│   ├── 05-personalized-learning/ 个性化学习
│   ├── 06-learning-companion/   成长陪伴
│   └── 07-smart-classroom/      AI 智慧课堂
├── scripts/                  构建与文档检查
└── docs/                     维护说明与写作安排
```

新领域完成具体案例后，再作为独立目录加入这里。教育篇的[写作安排](docs/plans/2026-10-12-education-rewrite-design.md)记录当前范围与推进顺序。

---

[Blueberry](https://github.com/lizhe-0423) · AI Agent Engineer · [掘金](https://juejin.cn/user/1420997038194350)
