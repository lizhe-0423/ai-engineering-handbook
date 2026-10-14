# AI 教育解决方案

[← 返回首页](../README.md)

这一部分整理 AI 教育公司的产品与工程问题。文章从一次真实业务请求怎样进入系统写起，讲清数据从哪里来，模型和 Agent 怎样配合，教师或校务人员在哪一步确认结果，以及产品上线后该看哪些指标。

这里不会按大模型、数字人、知识图谱等技术名词分目录。同一种技术可能同时服务答疑、备课和校务咨询，业务责任却完全不同。目录按使用者正在完成的工作划分。

| 业务场景 | 场景说明 | 对应文章及内容 |
|---|---|---|
| [数字名师与智能学习服务](digital-teacher/README.md) | 面向学生的课程内答疑、辅导和学习路径安排 | [数字名师怎样回答一道题](digital-teacher/qa.md)讲题目识别、课程检索、教学策略和拒答边界。[个性化学习从学习记录开始](digital-teacher/personalized-learning.md)讲知识点映射、学习者状态、推荐约束和后续评测。[学生档案怎样成为长期记忆](digital-teacher/student-profile-memory.md)讲 Markdown 档案、会话压缩和跨会话更新。 |
| [教师智能助手](teacher-assistant/README.md) | 面向教师和教研员的备课、资源加工与方案复核 | [智能备课怎样接进教师原有流程](teacher-assistant/lesson-planning.md)讲资料权限、Agent 工作流、版本差异和教师确认。 |
| [AI 智慧课堂与实践教学](smart-classroom/README.md) | 面向正在发生的课堂、实验和实训，强调实时配合 | [AI 实时视频教学怎样进入课堂](smart-classroom/realtime-video-teaching.md)讲脚本、课件、音视频同步、延迟降级和真人接管。 |
| [智能作业与教育评价](assessment/README.md) | 面向作答处理、反馈和评价复核 | [智能批改要留下可以复核的依据](assessment/grading.md)讲输入校验、评分量规、证据链、复核队列和一致性评测。 |
| [学生成长与生涯服务](student-development/README.md) | 面向较长周期的计划跟进、求助和风险转介 | [学习陪伴先从一项任务做起](student-development/learning-companion.md)讲记忆边界、未成年人隐私、风险分级和人工响应。 |
| [学校运营与教育治理](school-operations/README.md) | 面向招生、教务和校园服务的咨询与事项办理 | [校园服务 Agent 怎样安全地办一件事](school-operations/campus-service-agent.md)讲意图识别、权限、工具调用、幂等和审计。 |

读这些文章时，可以把一条共同的判断线放在心里。模型输出流畅，只能说明交互像样。教育产品是否可用，还要看资料是否可靠，流程能否回退，人工责任是否清楚，结果有没有帮助学习或完成业务。
