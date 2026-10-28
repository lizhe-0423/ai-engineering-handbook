# AI Agent 学习路线

[← 返回首页](../README.md)

从一次模型调用开始，逐步理解工具调用、知识检索和任务编排，再处理运行与恢复。这里按八个主题组织文章，基础机制写清以后，再把它们串成完整任务。

可以先看 [AI Agent 图解书](eli5/README.md)（覆盖 28 个主题及 2 篇架构补充）。每篇从一个具体问题出发，用对应机制的图形比较不同情况，再进入工程文章。GitHub 可以直接阅读图文版；离线 HTML 版支持情境切换、图解放大和章节搜索。

外部知识的加工维护放在知识工程，研发团队的流程与平台设计放在 [AI Native 研发实践](../ai-native/README.md)。学习路线通过链接衔接已有文章。

## 01　大模型应用基础

先接通模型，分清消息、输出与应用状态。流式响应和结构化结果放在具体调用过程中解释。

- [一次模型调用怎样从请求走到可用结果](model-calls-and-messages.md)从一次请求与响应开始，说明角色消息、流式输出、结构化结果和调用失败的处理。 [图解](eli5/chapters/01.md)
- [提示词怎样成为可检查的任务要求](prompt-task-contracts.md)区分角色、背景、任务与约束，通过示例与反例检查规则，并说明提示词、材料分隔和程序校验各自承担的范围。 [图解](eli5/chapters/02.md)

## 02　工具调用与行动循环

先看一次工具调用怎样完成，再让模型根据工具结果决定下一步。MCP 和 Skill 随后接入，不要求第一版就使用完整框架。

- [Function Calling 怎样完成一次工具调用](function-calling.md)讲工具声明、参数校验、受控执行与结果回填，区分调用标识、业务权限与幂等，并用只读查询串起完整过程。 [图解](eli5/chapters/03.md)
- [ReAct 怎样根据观察结果继续行动](react-observation-loop.md)讲判断、行动与观察怎样构成循环，以及何时结束或停止尝试。 [图解](eli5/chapters/04.md)
- [MCP 怎样接入外部工具](mcp-external-tools.md)讲客户端与服务端、能力发现和调用过程，区分协议接入与模型工具调用。 [图解](eli5/chapters/05.md)
- [Skill 怎样加载和参与执行](skill-loading-and-execution.md)讲入口、按需加载、版本维护，以及 Skill 与工具的配合和执行边界。 [图解](eli5/chapters/06.md)
- [工具注册表怎样管理能力生命周期](tool-registry-lifecycle.md)讲统一工具契约、注册与发现，以及注销时怎样处理正在执行的调用。 [图解](eli5/chapters/07.md)

## 03　上下文、记忆与知识

分清本轮模型需要的材料、跨会话保留的记忆，以及有来源的外部知识。检索与维护各有独立职责。

- [Agent 怎样管理上下文与长期记忆](context-and-long-term-memory.md)讲窗口预算、摘要压缩、记忆读写与纠错，区分模型上下文和恢复任务所需的正式状态。 [图解](eli5/chapters/08.md)
- [RAG 怎样从检索材料走到有依据的回答](rag-evidence-and-answers.md)讲资料切分、关键词与向量检索、结果筛选和引用核对，也保留检索失败与资料冲突的处理。 [图解](eli5/chapters/09.md)
- [Wiki 式知识编译与增量维护](../enterprise-ai-platform/knowledge-engineering/wiki-knowledge-maintenance.md)归属知识工程，讲有来源的知识条目、增量修订、冲突与下架处理。 [图解](eli5/chapters/10.md)

文档处理的已有文章见[复杂文档怎样解析、转换并通过验收](../enterprise-ai-platform/knowledge-engineering/document-conversion.md)，检索索引的更新见[向量索引怎样和业务数据保持一致](../enterprise-ai-platform/knowledge-engineering/vector-index-lifecycle.md)。两篇作为相关工程能力继续复用。

## 04　路由、工作流与协作

先判断任务能否用明确分支和固定步骤完成，再考虑动态委派。单个 Agent、多角色协作与跨服务通信分别讨论。

- [意图识别怎样进入请求路由](intent-routing.md)讲分类、未知意图与歧义处理，以及程序怎样验证分类结果后再分发。 [图解](eli5/chapters/11.md)
- [工作流状态机怎样控制任务推进](workflow-state-machine.md)讲节点、条件边、状态保存与恢复，说明固定编排和模型动态选择的边界。 [图解](eli5/chapters/12.md)
- [多 Agent 怎样分工并交付共同结果](multi-agent-collaboration.md)讲任务契约、结构化消息、结果检查，以及协作增加的成本与失败点。 [图解](eli5/chapters/13.md)
- [子代理怎样接受委派并返回结果](subagent-delegation.md)区分全新上下文与继承上下文，处理委派范围、并发限制、取消与结果回收。 [图解](eli5/chapters/14.md)
- [A2A 怎样连接不同服务中的 Agent](a2a-agent-cooperation.md)讲能力发现、远程任务状态与异步结果，区分通信成功和任务完成。 [图解](eli5/chapters/15.md)

## 05　运行时与任务可靠性

运行时负责推进执行并记录当前状态。达到上限、工具失败或进程重启，都需要有明确的结束或恢复方式。

- [受控运行时怎样管理回合与执行步骤](controlled-agent-runtime.md)覆盖 Turn、Step、结束原因、上下文预算、步数与时间上限，以及重试和兜底。 [图解](eli5/chapters/16.md)
- [事件记录怎样支持状态恢复](event-state-recovery.md)讲追加日志、状态投影和检查点，区分回放记录与重新执行工具，处理重复事件和外部副作用。 [图解](eli5/chapters/17.md)

研发场景的架构背景可先读 [Agent Harness 怎样让长任务跑到结束](../ai-native/agent-harness-long-running-task.md)。

## 06　人机协同与安全

缺少信息、缺少授权和运行风险需要分别处理。安全检查从前面的示例开始加入，不等到全部功能写完。

- [澄清提问怎样挂起并恢复任务](clarification-and-resume.md)保存待回答问题与执行位置，校验人工答复，处理超时、取消和重复回复。 [图解](eli5/chapters/18.md)
- [审批门禁怎样约束高风险工具](approval-gates.md)讲审批范围、有效期限与撤销，审批期间任务或参数改变后重新校验。 [图解](eli5/chapters/19.md)
- [沙箱怎样隔离 Agent 的执行](agent-sandbox-isolation.md)区分应用层检查与执行环境隔离，展开文件、网络、进程和资源限制，不把命令黑名单当作完整安全保证。 [图解](eli5/chapters/20.md)

已有文章与架构背景如下。

- [Agent 服务怎样防止能力被批量提取](agent-service-security.md)讨论跨会话滥用、内容提取与持续防御。 [图解](eli5/chapters/21.md)
- [身份、权限和 Guardrail 怎样约束 Agent](../ai-native/agent-identity-policy-guardrail.md)提供身份委托与行动检查的架构说明。 [图解](eli5/chapters/29.md)
- [Agent 在哪里运行](../ai-native/agent-runtime-environment.md)提供隔离环境与运行生命周期的架构说明。 [图解](eli5/chapters/30.md)

## 07　可观测性与评测

保存执行证据，再按任务完成标准检查结果。评测贯穿各章示例，区分教学模拟、真实模型调用与实际环境验证。

- [怎样看清一次 Agent 执行](../ai-native/agent-observability-and-evaluation.md)讲轨迹采集、诊断与证据保留。 [图解](eli5/chapters/22.md)
- [Agent 评测怎样判断一次修改有没有真的变好](agent-evaluation.md)讲任务完成标准、轨迹约束、评分与版本对照。 [图解](eli5/chapters/23.md)

## 08　扩展机制与综合实践

前面的机制稳定以后，再扩展能力的装载方式和交互入口。综合实践最后检查它们是否能一起工作。

- [插件怎样安装、卸载并释放资源](plugin-lifecycle.md)讲插件契约、工具批量注册与注销、在途调用处理，以及加载隔离的边界。 [图解](eli5/chapters/24.md)
- [Hooks 怎样介入工具执行前后](hooks-tool-execution.md)讲拦截、参数修改、结果脱敏与审计，以及顺序、超时和钩子自身失败的处理。 [图解](eli5/chapters/25.md)
- [CLI Agent 怎样进入终端工作流](cli-agent-workflow.md)讲交互式会话、单次执行、工作目录、退出状态与取消机制。 [图解](eli5/chapters/26.md)
- [定时任务怎样可靠触发 Agent](scheduled-agent-tasks.md)讲一次性与周期调度、持久化、重复触发、服务重启恢复，以及取消与执行同时发生的处理。 [图解](eli5/chapters/27.md)
- [一个完整任务怎样串起 Agent 的各项机制](complete-agent-task.md)将路由、记忆、检索与工具接入受控运行时，保留人工分支，用失败场景与任务验收检查整条流程。 [图解](eli5/chapters/28.md)
