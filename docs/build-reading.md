# 生成本地阅读版

Markdown 正文和合订稿只需 Python 标准库：

```bash
python3 scripts/build_book.py
```

HTML 是可选的构建产物，生成后离线阅读，不依赖在线图片服务或网页运行时脚本。构建需要 Node.js、`marked`、`playwright`、Playwright 的 Chromium，以及预先准备的 Mermaid 浏览器单文件库。库和浏览器仅在构建阶段使用，不属于 Python 示例依赖。

```bash
# 如果本机尚未准备构建工具，可在独立工具目录安装
npm install marked playwright
npx playwright install chromium

# MERMAID_FILE 替换为本地 mermaid.min.js 的路径
node scripts/build_reading.cjs --mermaid MERMAID_FILE
```

Node 需要能够找到上述两个包；使用独立工具目录时可通过 `NODE_PATH` 指向其 `node_modules`。本次构建使用 Mermaid 11.12.0 的单文件浏览器库，下载入口见 [Mermaid 官方用法文档](https://mermaid.js.org/config/usage.html)；使用固定版本并遵守库的原许可。

如果使用已有 Chromium/Chrome 可执行文件，可通过 `FDE_BROWSER_EXECUTABLE` 指定路径。脚本创建新的无头浏览器会话，只读取本书生成的 HTML，不使用个人浏览器配置。

输出位于忽略跟踪的 `build/`：`reading.html`、各章流程图 SVG/PNG、桌面与移动截图，以及渲染结果。脚本遇到图语法错误会失败，不将未渲染代码当成流程图交付。

GitHub 阅读正文时使用 Mermaid 代码块；本地 HTML 采用已经渲染的 SVG。修改章节后，应依次重建合订稿和 HTML。
