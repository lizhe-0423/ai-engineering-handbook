# 图解书的内容与页面源文件

这套图解保留 HTML 和 Markdown 两种阅读形式。HTML 可以离线切换情况、放大机制图和检查理解；Markdown 方便在 GitHub 阅读同一套内容。

## 内容与构图

- `content.py` 保存 30 篇的讲解、三种情况、概念边界和理解题。
- `diagrams.py` 为每个主题单独定义构图。时序表示调用往返，依赖图表示知识更新，账本表示恢复，时间条表示执行轨迹，文档对照表示审批范围。
- `build.py` 同步生成文章、目录和 SVG，避免手改 HTML 后忘记同步 Markdown。
- `../guide.css` 统一字号、留白与导航，同时按讲解内容使用不同正文排布。
- `../guide.js` 只处理本地阅读交互，不发送网络请求，不连接模型或业务工具。

精确标签、方向和状态是这些机制图的重点，因此使用可编辑 SVG。每篇三个状态来自同一个明确例子，不能只更换颜色和结论；箭头、状态记录或相关内容必须跟着变化。统一阅读界面，不把不同概念压成统一的三格流程。第 17 篇的主题是事件账本，采用独立版式与回放台，模板见 `redesign_17.html`。

## 构建与静态检查

在仓库根目录运行，Python 使用标准库即可。

```sh
python3 agent-learning-path/eli5/source/build.py
python3 agent-learning-path/eli5/source/check.py
node --check agent-learning-path/eli5/guide.js
```

构建器只清理上一版生成的指定图解资产，不处理工程文章或其他文件。直接修改生成的 HTML、Markdown 或 SVG 会被下一次构建覆盖，应修改对应源文件。

## 浏览器检查

`browser-check.cjs` 使用本机已有的 Playwright 和 Chromium，不负责安装或下载。通过环境变量传入模块与浏览器路径。

```sh
AGENT_GUIDE_PLAYWRIGHT=/absolute/path/to/node_modules/playwright \
AGENT_GUIDE_CHROME=/absolute/path/to/chromium \
AGENT_GUIDE_SCREENSHOTS=/tmp/agent-guide-review \
node agent-learning-path/eli5/source/browser-check.cjs
```

如果 Node.js 已经可以找到 Playwright，且已有配套 Chromium，可以省略前两项。输出目录用于保存截图和检查报告，不应提交截图缓存。

检查覆盖目录搜索、筛选、30 篇的情境切换、理解题、键盘操作、放大与关闭，以及桌面、平板和手机尺寸。第 17 篇使用独立账本页，脚本改查三种恢复情况、外部核对与理解题。90 张 SVG 逐张检查文本边界与可见文本重叠，并生成联系表供人工检查方向、构图和内容。自动检查不能代替阅读图中的含义。

所有例子与图中状态都用于教学，验证结果只代表图解的排版与本地交互，不代表真实 Agent、模型或业务系统已经通过测试。
