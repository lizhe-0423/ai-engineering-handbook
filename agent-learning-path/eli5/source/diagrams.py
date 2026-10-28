"""Thirty topic-specific diagram compositions, with three teaching states each.

Geometry is intentional: timelines, documents, circuits, maps, tables and enclosures
encode different relationships. The SVG is the editable, accessible source asset.
"""
from html import escape

INK = "#202b32"
MUTED = "#667273"
PAPER = "#f6f3eb"
LINE = "#d8dcd5"
BLUE = "#2858ce"
GREEN = "#287260"
RED = "#bc492e"
GOLD = "#b67e21"
WHITE = "#fffefa"


class Drawing:
    def __init__(self, title, desc, accent, dark=False):
        self.parts = []
        self.title, self.desc, self.accent, self.dark = title, desc, accent, dark
        self.ink = "#f4f2e9" if dark else INK
        self.muted = "#acb9bb" if dark else MUTED
        self.bg = "#18272e" if dark else PAPER
        self.rect(0, 0, 1000, 540, self.bg)

    def rect(self, x, y, w, h, fill=WHITE, stroke="none", r=0, opacity=1):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" opacity="{opacity}"/>')

    def text(self, x, y, value, size=22, color=None, weight=400, anchor="start", mono=False):
        family = "ui-monospace, SFMono-Regular, Menlo, monospace" if mono else "-apple-system, BlinkMacSystemFont, PingFang SC, Microsoft YaHei, sans-serif"
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color or self.ink}" font-family="{family}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')

    def circle(self, x, y, radius, fill=WHITE, stroke=LINE, width=2):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def path(self, value, color=LINE, width=2, arrow=False, dash=False, fill="none"):
        self.parts.append(f'<path d="{value}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="7 8"' if dash else '')+'/>')

    def line(self, x, y, x2, y2, color=LINE, width=2, arrow=False, dash=False):
        self.path(f"M{x},{y} L{x2},{y2}", color, width, arrow, dash)

    def pill(self, x, y, label, color=None, width=None):
        color = color or self.accent
        w = width or max(88, len(label) * 18 + 28)
        self.rect(x, y, w, 34, color, r=17)
        self.text(x + w / 2, y + 23, label, 17, WHITE, 600, "middle")

    def label(self, x, y, title, sub="", color=None, anchor="start"):
        self.text(x, y, title, 25, color, 650, anchor)
        if sub:
            self.text(x, y + 32, sub, 18, self.muted, 400, anchor)

    def note(self, value, color=None):
        self.line(42, 482, 958, 482, "#405158" if self.dark else LINE)
        self.text(42, 516, value, 21, color or self.muted)

    def paper(self, x, y, w, h, title, lines=(), accent=None):
        self.rect(x + 7, y + 8, w, h, "#122028" if self.dark else "#e5e5dc", r=3)
        self.rect(x, y, w, h, "#263941" if self.dark else WHITE, "#405158" if self.dark else LINE, 3)
        self.rect(x, y, 5, h, accent or self.accent)
        self.text(x + 22, y + 39, title, 23, weight=650)
        self.line(x + 22, y + 57, x + w - 22, y + 57, "#405158" if self.dark else LINE)
        for i, val in enumerate(lines):
            self.text(x + 22, y + 91 + i * 35, val, 20, self.muted)

    def node(self, x, y, label, active=False, radius=42):
        self.circle(x, y, radius, self.accent if active else self.bg, self.accent if active else LINE)
        self.text(x, y + 7, label, 21, WHITE if active else self.ink, 650, "middle")

    def finish(self):
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="540" viewBox="0 0 1000 540" role="img" aria-labelledby="title desc">
<title id="title">{escape(self.title)}</title><desc id="desc">{escape(self.desc)}</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs>
{''.join(self.parts)}</svg>'''


def render(c, s, accent):
    n = int(c["id"])
    dark = n in (7, 16, 17, 22, 26)
    d = Drawing(c["title"] + " · " + c["states"][s][0], c["states"][s][1], accent, dark)
    RENDERERS[n](d, s)
    return d.finish()


def request(d, s):
    d.text(46, 44, "一份请求的流转", 18, d.muted)
    d.paper(50, 85, 300, 300, "应用准备的请求", ["周五整理接口清单", "负责人" + ("  蓝莓" if s == 0 else "  未确定")])
    d.text(75, 343, "规则 · 不补写未知信息", 19, BLUE)
    d.line(365, 235, 430, 235, BLUE, 3, True)
    d.text(398, 205, "请求", 18, BLUE, 600, "middle")
    d.circle(498, 235, 57, "#e6ecfa", "none")
    d.text(498, 244, "模型", 28, BLUE, 650, "middle")
    d.line(565, 235, 635, 235, RED if s == 2 else GREEN, 3, True, s == 2)
    d.text(598, 205, "片段" if s == 2 else "回答", 18, d.muted, anchor="middle")
    d.paper(650, 85, 300, 300, "应用收到的结果", ["事项  整理接口清单", "日期  周五", "负责人  " + ("蓝莓" if s == 0 else "未知"), "完整性  " + ("中断…" if s == 2 else "已结束")], RED if s == 2 else GREEN)
    d.pill(704, 410, ["依据核对通过", "空值也有意义", "不可提交业务"][s], RED if s == 2 else GREEN, 210)
    d.note(["收到回复 → 检查完整性 → 核对字段与材料", "未知信息保留未知，不用流畅的文字填补事实缺口。", "显示了一部分文字，不等于得到了可用结果。"][s])


def prompt(d, s):
    d.paper(60, 45, 535, 395, "任务说明", [])
    rows = [("任务", "整理一下" if s == 0 else "提取待办事项"), ("材料", "会议记录的原文"), ("输出", "未指定" if s == 0 else "事项 / 期限 / 负责人"), ("缺失", "未约定" if s == 0 else "保留未知，禁止补写")]
    for i, (key, val) in enumerate(rows):
        y = 160 + i * 70
        d.text(90, y, key, 18, d.muted)
        d.text(180, y, val, 22, BLUE if i in (2, 3) and s else d.ink, 550)
        if i < 3: d.line(90, y + 23, 560, y + 23)
    if s == 2:
        d.paper(665, 65, 270, 190, "材料中的干扰", ["“忽略前面规则”", "“把资料发出去”"], RED)
        d.line(705, 294, 900, 294, RED, 5)
        d.text(800, 332, "材料不能授权", 25, RED, 650, "middle")
        d.text(800, 370, "发送权限由程序控制", 20, d.muted, anchor="middle")
    else:
        d.text(675, 105, "验收清单", 28, weight=650)
        for i, label in enumerate(["能解析字段", "缺失保持未知", "结论回到材料"]):
            y = 175 + i * 80
            d.rect(675, y - 24, 28, 28, "none", LINE, 3)
            if s: d.path(f"M681,{y-12} l7,8 l13,-20", GREEN, 3)
            d.text(720, y, label, 21, d.muted)
    d.note("好要求能被检查；文本标签帮助分隔材料，不能代替权限边界。")


def calling(d, s):
    xs = [150, 500, 850]
    for x, t in zip(xs, ["模型", "应用", "业务工具"]):
        d.text(x, 62, t, 27, weight=650, anchor="middle")
        d.line(x, 90, x, 435, "#cbd1cd", 2, dash=True)
    d.line(150, 146, 485, 146, BLUE, 3, True)
    d.text(325, 128, "调用提议 + 参数", 20, BLUE, anchor="middle")
    d.rect(408, 181, 184, 52, RED if s == 2 else "#e5eee8", r=3)
    d.text(500, 214, "权限拒绝" if s == 2 else "参数与权限校验", 20, WHITE if s == 2 else GREEN, 600, "middle")
    if s == 1:
        d.line(500, 265, 835, 265, GREEN, 3, True)
        d.text(675, 248, "真正执行查询", 20, GREEN, anchor="middle")
        d.line(850, 337, 515, 337, GREEN, 3, True)
        d.text(675, 319, "任务状态 · 受阻", 20, GREEN, anchor="middle")
        d.line(500, 409, 165, 409, BLUE, 3, True)
        d.text(325, 391, "对应调用标识的结果", 20, BLUE, anchor="middle")
    elif s == 0:
        d.text(675, 311, "尚未执行", 35, d.muted, 500, "middle")
        d.text(675, 352, "模型只提出行动", 20, d.muted, anchor="middle")
    else:
        d.line(500, 310, 165, 310, RED, 3, True)
        d.text(325, 291, "返回拒绝状态", 20, RED, anchor="middle")
        d.text(850, 340, "未调用", 28, RED, 600, "middle")
    d.note("模型提议 → 应用校验 → 工具执行 → 结果回填，各有自己的责任。")


def react(d, s):
    for i,path in enumerate(["M310,145 Q500,15 690,145", "M750,220 Q810,390 550,407", "M425,407 Q185,370 247,220"]):
        d.path(path, d.accent if s==0 or i==2 else LINE, 4 if s==0 or i==2 else 2, True)
    d.node(275, 180, "判断", True, 60)
    d.node(730, 180, "行动", s == 0, 60)
    d.node(490, 405, "观察", s == 2, 60)
    d.text(500, 155, "查任务状态", 22, anchor="middle")
    d.text(500, 217, ["受阻，原因未知", "状态与原因已确认", "再次出现相同错误"][s], 27, weight=600, anchor="middle")
    d.pill(378, 249, ["再查阻塞记录", "证据够了，结束", "达到上限，停止"][s], [d.accent, GREEN, RED][s], 244)
    if s != 0:
        d.line(206, 180, 76, 180, GREEN if s == 1 else RED, 3, True)
        d.text(105, 225, "出口", 21, GREEN if s == 1 else RED, anchor="middle")
    d.note("每次继续都应有新理由；回答、澄清和停止都是合法出口。")


def mcp(d, s):
    d.rect(45, 67, 540, 367, "#e7eaf0", r=8)
    d.text(70, 105, "Agent 应用 · Host", 23, BLUE, 650)
    d.rect(73, 145, 199, 93, WHITE, r=3)
    d.text(172, 184, "模型", 26, weight=650, anchor="middle")
    d.text(172, 214, "只看到被提供的定义", 16, d.muted, anchor="middle")
    d.rect(320, 145, 234, 93, WHITE, r=3)
    d.text(437, 184, "工具目录与筛选", 23, weight=650, anchor="middle")
    d.text(437, 214, "应用控制开放范围", 17, d.muted, anchor="middle")
    d.rect(320, 304, 234, 89, BLUE, r=3)
    d.text(437, 357, "MCP Client", 25, WHITE, 650, "middle")
    d.paper(735, 140, 215, 250, "MCP Server", ["提供能力", "处理工具请求", "返回真实结果"])
    if s == 1:
        d.line(437, 251, 437, 293, BLUE, 3, True)
    else:
        d.line(437, 300, 437, 251, BLUE, 3, True)
    if s == 1:
        d.line(272, 191, 307, 191, GREEN, 3, True)
        d.text(292, 134, "提议", 17, GREEN, anchor="middle")
        d.line(554, 334, 721, 334, GREEN, 3, True)
        d.text(641, 313, "tools/call", 20, GREEN, 650, "middle", True)
        d.line(735, 372, 566, 372, GREEN, 2.5, True)
        d.text(644, 405, "工具结果", 18, GREEN, anchor="middle")
        d.path("M320,350 H170 V253", GREEN, 2.5, True)
        d.text(173, 411, "应用按标识回填", 17, GREEN, anchor="middle")
    else:
        d.line(554, 334, 721, 334, BLUE, 3, True)
        d.text(644, 312, "tools/list", 20, BLUE, 650, "middle", True)
        d.line(735, 372, 566, 372, GREEN, 2.5, True)
        d.text(644, 405, "工具定义", 18, GREEN, anchor="middle")
        d.line(320, 191, 285, 191, LINE, 2, True, True)
        d.text(292, 133, "按需提供", 17, d.muted, anchor="middle")
    d.pill(733, 70, "本机子进程" if s == 2 else "远程工具服务", d.accent, 220)
    if s == 2:
        d.path("M30,47 H971 V458 H30 Z", LINE, 2, dash=True)
        d.text(70, 477, "同一台机器", 17, d.muted)
    d.note("stdio · 本机进程也能提供 MCP 服务" if s == 2 else "发现工具、提供上下文、执行工具，是三个不同动作。")


def skill(d, s):
    stages = [(65, 95, 240, 300, "01 / 封面", "名称与描述", ["task-weekly-report", "适合整理任务周报"]), (365, 69, 260, 350, "02 / 做法", "SKILL.md", ["确认日期", "查询任务", "保留未知，检查草稿"]), (690, 113, 240, 270, "03 / 资源", "按步骤读取", ["规则与模板", "允许的检查脚本"])]
    for i, (x,y,w,h,k,t,ls) in enumerate(stages):
        d.paper(x,y,w,h,t,ls, d.accent if i <= s else LINE)
        d.text(x+15, y-19, k, 19, d.accent if i <= s else d.muted)
    d.line(310, 260, 355, 260, d.accent, 3, True)
    d.line(630, 260, 680, 260, d.accent if s else LINE, 3, True)
    if s == 2:
        d.rect(373, 262, 242, 79, "#f7e4dd", r=3)
        d.text(494, 294, "查询工具不可用", 22, RED, 650, "middle")
        d.text(494, 323, "方法仍在，行动受限", 18, RED, anchor="middle")
    d.note(["先看适用场景，避免每个请求都载入整套说明。", "只有被读取的做法与材料，才成为当前任务的上下文。", "Skill 描述怎么做，工具与权限决定哪些步骤能执行。"][s])


def registry(d, s):
    d.text(45, 57, "TOOL REGISTRY", 23, "#a8c7e9", 600, mono=True)
    d.text(45, 94, "能力目录", 32, weight=650)
    cols = [54, 385, 550, 745]
    for x, t in zip(cols, ["工具 / 来源", "版本", "状态", "新调用 / 在途"]): d.text(x, 157, t, 19, d.muted)
    d.line(45, 176, 954, 176, "#405158")
    for i, row in enumerate([("tasks / MCP", "v2", ["ACTIVE", "DRAINING", "REMOVED"][s], ["允许 / 2", "拒绝 / 2", "拒绝 / 0"][s]), ("pdf / 本地", "v1", "ACTIVE", "允许 / 0"), ("search / HTTP", "v3", "ACTIVE", "允许 / 1")]):
        y = 229 + i*76
        if i == 0: d.rect(45, y-36, 909, 60, "#293e47", r=3)
        for j,(x,val) in enumerate(zip(cols,row)): d.text(x,y,val,22,"#e9b69c" if i == 0 and j>1 else d.ink,mono=j in (1,2))
    d.pill(45, 405, ["按权威状态执行", "等待在途调用结束", "资源已释放"][s], GREEN if s == 0 else d.accent, 260)
    d.note("停止接新调用 → 排空已有调用 → 注销；本地函数和 MCP 工具都能登记。")


def memory(d, s):
    d.text(55, 64, "这一轮的工作桌面", 29, weight=650)
    d.rect(48, 94, 535, 306, "#e4ebe2", r=8)
    cards = [(75,120,210,112,"本次问题","生成这周周报"),(310,120,245,112,"必要规则","只使用有依据的信息"),(75,252,480,120,"较早的会话" if s == 0 else "压缩后的摘要","详细历史占用窗口" if s == 0 else "保留约束、待确认项和证据引用")]
    for x,y,w,h,t,v in cards:
        d.rect(x,y,w,h,WHITE, r=3);d.text(x+16,y+34,t,22,weight=600);d.text(x+16,y+75,v,18,d.muted)
    d.line(48,421,583,421,LINE,7)
    d.line(48,421,[510,330,355][s],421,GREEN,7)
    d.text(48,455,"窗口占用示意 · 还要给输出留出空间",19,GREEN)
    d.rect(715,94,230,306,"#dadfd5",r=4)
    d.text(830,64,"长期档案",29,weight=650,anchor="middle")
    for i,t in enumerate(["偏好", "来源", "更新时间"]):
        y=112+i*92;d.rect(732,y,196,76,WHITE,LINE,3);d.line(802,y+13,858,y+13,LINE,3);d.text(830,y+49,t if s != 2 or i else "纠正旧偏好",22,GREEN if s==2 and i==0 else d.ink,anchor="middle")
    d.line(705,187,594,187,GREEN,3,True);d.text(650,155,"按需取用",18,GREEN,anchor="middle")
    if s==2:d.path("M582,343 H650 V360 H706",RED,3,True);d.text(649,394,"核对后更新",18,RED,anchor="middle")
    d.note("正式任务状态另外保存；聊天摘要不负责证明某次发送是否成功。")


def rag(d, s):
    d.paper(45, 70, 405, 355, "检索材料 · 手册", ["适用范围  " + ("出差报销" if s==2 else "员工请假"), "版本  当前有效"])
    if s==1:
        d.text(82,252,"现行规定 · 提前三天",22,GREEN)
        d.rect(66,281,363,110,"#f6e2d8",r=3);d.text(85,317,"旧版本另有不同规定",23,RED,600);d.text(85,359,"生效范围需要确认",21,RED)
    elif s==2:
        d.rect(66,205,363,177,PAPER,r=3);d.text(85,252,"找到的是报销规则",25,RED,600);d.text(85,300,"没有请假时限的依据",21,d.muted)
    else:
        d.rect(67,237,360,60,"#dfedd7",r=2);d.text(82,275,"本例规定提前三天申请",23,GREEN,600)
    d.line(473,258,552,258,GREEN if s==0 else RED,3,True)
    d.text(515,227,"核对",18,d.muted,anchor="middle")
    d.paper(575,104,375,282,"准备给用户的回答",["请提前三天申请 [1]" if s==0 else "暂不下确定结论", "" if s==0 else ["","存在不同版本","资料未覆盖问题"][s]])
    if s==0:
        d.path("M815,235 V405 H240 V318",GREEN,2,dash=True)
        d.text(700,442,"[1] 真正支持这句话",21,GREEN,anchor="middle")
    d.note("示意规则为虚构例子。相关、现行、可访问、有依据，分别检查。")


def wiki(d, s):
    sources=[(95,120,"源文件 A"),(95,325,"源文件 B")]
    for x,y,t in sources:
        d.paper(x,y,200,112,t,["已更新" if s==1 and t.endswith("A") else "已下架" if s==2 and t.endswith("A") else "保留版本"],RED if s and t.endswith("A") else GREEN)
    links=[(295,177,480,130),(295,177,480,290),(295,383,480,290),(295,383,480,425)]
    for x,y,x2,y2 in links:d.path(f"M{x},{y} C385,{y} 385,{y2} {x2},{y2}",RED if s and y==177 else GREEN,3,True)
    for i,(y,t) in enumerate([(130,"知识条目 1"),(290,"知识条目 2"),(425,"知识条目 3")]):
        affected=s and i<2;d.circle(510,y,20,RED if affected else GREEN,"none");d.text(553,y+7,t,26,weight=600);d.text(775,y+7,"待复核" if s==1 and affected else "限制使用" if affected else "有效",22,RED if affected else GREEN)
    d.text(95,70,"来源",26,weight=650);d.text(480,70,"整理后的知识",26,weight=650)
    d.note("沿依赖关系找影响范围；来源的内容、版本与权限都可能变化。")


def routing(d, s):
    d.paper(45,180,275,180,"用户请求",[["查任务状态","有明确任务编号"],["处理一下任务","操作含糊"],["查状态并改负责人","包含两件事"]][s])
    d.line(330,266,455,266,d.accent,4,True)
    d.circle(495,266,30,d.accent,"none")
    outs=[(820,107,"只读查询"),(820,252,"澄清信息"),(820,397,"修改请求")]
    for i,(x,y,t) in enumerate(outs):
        active=(s==0 and i==0) or (s==1 and i==1) or (s==2 and i in(0,2))
        d.path(f"M525,266 C660,266 650,{y} 762,{y}",d.accent if active else LINE,5 if active else 2,True)
        d.circle(x,y,51,d.accent if active else WHITE,"none")
        d.text(x,y+7,["查","问","改"][i],31,WHITE if active else d.muted,600,"middle")
        d.text(x,y+73,t,21,d.ink,anchor="middle")
    d.text(485,205,"验证分类",22,d.accent,600,anchor="middle")
    d.note("分类范围、参数与权限由程序检查；含糊与未知都有自己的出口。")


def workflow(d, s):
    pts={"开始":(95,255),"范围":(290,255),"查询":(490,255),"草稿":(690,255),"交付":(900,255),"等待":(290,100),"修订":(690,410)}
    for a,b in zip(["开始","范围","查询","草稿"],["范围","查询","草稿","交付"]):
        x,y=pts[a];xx,yy=pts[b];d.line(x+43,y,xx-48,yy,d.accent if s==0 else LINE,3,True)
    d.path("M290,210 V150",d.accent if s==1 else LINE,3,True)
    d.path("M335,100 H380 V220 H329",d.accent if s==1 else LINE,2,True)
    d.path("M690,300 V360",d.accent if s==2 else LINE,3,True)
    d.path("M643,410 H598 V310 L651,282",d.accent if s==2 else LINE,2,True)
    selected=["草稿","等待","修订"][s]
    for t,(x,y) in pts.items():d.node(x,y,t,t==selected)
    d.text(45,43,"任务状态地图",28,weight=650)
    d.text(472,111,"信息补齐后返回",20,d.muted)
    d.text(724,381,"检查未通过",18,d.muted)
    d.note("一个位置表示一种状态；只有条件满足，才允许沿边进入下一步。")


def teamwork(d, s):
    labels=["查询 Agent", "写作 Agent", "审查 Agent"]
    for i,t in enumerate(labels):
        y=70+i*130;d.text(48,y+42,t,23,weight=650);d.line(220,y+79,950,y+79)
    d.rect(245,75,195,65,"#dbe8f7",r=4);d.text(342,115,"事实 + 来源",23,BLUE,600,"middle")
    d.path("M440,108 H488 V237 H545",RED if s==1 else BLUE,3,True)
    d.rect(550,205,185,65,"#e7e0f2",r=4);d.text(642,245,"周报草稿",23,d.accent,600,"middle")
    d.path("M735,237 H775 V368 H815",d.accent,3,True)
    d.rect(820,335,130,65,"#e2eddf",r=4);d.text(885,375,"验收",23,GREEN,600,"middle")
    if s==1:
        d.rect(245,152,194,39,"#f5e2d8",r=3);d.text(342,179,"一项查询失败",18,RED,600,"middle");d.text(561,302,"缺口随交付物传递",20,RED)
    elif s==2:
        d.path("M820,415 H640 V284",RED,3,True);d.text(738,447,"退回无依据结论",20,RED,anchor="middle")
    else:d.text(308,447,"每次交接都带范围、产物与证据",24,d.muted)
    d.note("角色增加了交接；共同结果仍要统一验收。")


def subagent(d, s):
    d.rect(52,61,340,369,"#e9e4ee",r=6);d.text(78,107,"主任务上下文",27,weight=650)
    for i,t in enumerate(["用户目标","长期对话","其他资料","本次子任务"]):
        d.rect(78,133+i*66,286,49,WHITE,r=3);d.text(97,166+i*66,t,21,d.accent if i==3 else d.muted)
    d.path("M392,356 H502 V160 H604",RED if s==2 else d.accent,3,True)
    if s==1:d.path("M392,223 H475 V208 H604",d.accent,2,True,True)
    d.rect(620,86,330,266,WHITE,LINE,6);d.text(644,130,"子代理的任务包",26,weight=650)
    for i,t in enumerate(["只核对三项任务", "来源与检查规则", "筛选后的相关历史" if s==1 else "不带无关历史"]):d.text(644,187+i*49,t,22,d.muted)
    d.path("M785,363 V420 H408",RED if s==2 else GREEN,3,True)
    d.text(620,451,"取消通知与结果核对" if s==2 else "结果 + 来源 + 未解决项",22,RED if s==2 else GREEN,anchor="middle")
    d.note("传递必要背景，限定权限与预算；主代理负责接收和检查返回结果。")


def a2a(d, s):
    d.rect(45,87,260,340,"#e9e4ee",r=6);d.label(175,143,"调用方服务","准备接入" if s==0 else "本地任务 A",anchor="middle")
    d.rect(695,87,260,340,"#e9e4ee",r=6);d.label(825,143,"远端 Agent","能力入口" if s==0 else "远端任务 B",anchor="middle")
    d.line(330,230,674,230,d.accent,3,True,s==2)
    d.text(500,207,["读取 Agent Card","提交明确任务","提交后连接超时"][s],22,d.accent,anchor="middle")
    d.line(674,325,330,325,RED if s==2 else GREEN,3,True,s==2)
    d.text(500,303,["能力与接入信息","返回任务标识 / 状态","回执未知"][s],21,RED if s==2 else GREEN,anchor="middle")
    d.text(175,233,"核对能力" if s==0 else "保存关联",24,weight=600,anchor="middle");d.text(175,278,"发现阶段" if s==0 else "A ↔ B",26,d.accent,650,"middle",s!=0)
    d.text(825,236,["能力发现","运行中","可能仍在运行"][s],22,weight=600,anchor="middle")
    d.text(825,282,"查询 / 更新 / 产物",18,d.muted,anchor="middle")
    d.text(500,415,"跨越网络与服务边界",20,d.muted,anchor="middle")
    d.note("这里示意异步任务；具体服务也可能直接返回结果。超时后先核对。")


def runtime(d, s):
    d.text(45,60,"TURN 01",28,"#bdd3e2",600,mono=True);d.text(225,59,"回答任务为什么受阻",23)
    d.rect(45,100,590,313,"#243a43",r=4)
    steps=["模型 · 选择查询", "工具 1 · 查询任务状态", "模型 · 判断缺少原因", "工具 2 · 查询阻塞记录", ["下一步 · 尚未启动", "工具 3 · 重试仍失败", "取消 · 停止启动新步骤"][s]]
    for i,t in enumerate(steps):
        y=145+i*58;d.circle(80,y-8,10,GREEN if i<3 else GOLD if i==3 else RED if s else "#405158","none");d.text(112,y,t,22)
    d.text(700,140,"工具调用预算",23,d.muted)
    for i in range(3):d.rect(704+i*76,175,59,95,"#94b6a7" if i<(3 if s==1 else 2) else "#405158",r=3)
    d.text(811,323,"3 / 3" if s==1 else "2 / 3",43,"#f1d79e" if s==1 else d.ink,600,"middle",True)
    d.pill(684,363,["可进入下一步","预算耗尽","用户已取消"][s],GREEN if s==0 else RED,240)
    d.note("示意上限为三次工具调用，重试计入预算；上限由程序执行。")


def events(d, s):
    d.text(48,61,"APPEND-ONLY / 事件账本",25,"#bdd3e2",600)
    ev=["任务已创建","查询结果已保存","草稿已生成","发送请求已发出"]
    for i,t in enumerate(ev):
        y=121+i*77;d.text(53,y,f"0{i+1}",22,"#87a7ad",mono=True);d.text(109,y,t,23);d.line(48,y+26,440,y+26,"#405158")
    if s==1:
        d.rect(45,77,410,140,"#4b6c66",r=3,opacity=.25);d.pill(60,411,"检查点 · 已处理到 02",GREEN,330)
    d.line(466,248,620,248,"#9dc2ad",3,True);d.text(545,215,"只计算状态",19,"#9dc2ad",anchor="middle")
    d.paper(651,102,300,300,"恢复出的当前状态",["草稿存在", "查询证据已保存", "发送结果" + ("  未知" if s==2 else "  待核对")])
    if s==2:d.pill(666,350,"先查询外部状态",RED,270)
    d.note("重放记录 ≠ 再执行历史动作。缺回执时，不要凭日志猜成功或失败。")


def clarification(d, s):
    d.text(57,66,"用户",23,weight=650);d.text(405,66,"对话",23,weight=650);d.text(783,66,"任务状态",23,weight=650)
    d.rect(55,100,430,75,"#e3ebdf",r=20);d.text(80,146,"帮我写一份周报",27)
    d.rect(151,204,438,75,WHITE,LINE,20);d.text(178,251,"需要哪一周的日期范围？",25)
    d.line(612,240,702,240,d.accent,3,True)
    d.paper(725,122,230,285,"保存书签",["任务 T-01", "问题 Q-01", ["等待日期", "日期已确认", "任务已取消"][s], ["恢复到查询", "继续进入查询", "不再恢复执行"][s]])
    if s:
        d.rect(55,315,430,75,"#e3ebdf",r=20);d.text(80,361,"本周一到周五",26)
        d.pill(110,416,"答复有效，继续" if s==1 else "任务已取消，忽略旧回复",GREEN if s==1 else RED,350)
    else:d.pill(151,344,"等待期间可释放执行线程",GOLD,382)
    d.note("回答要关联当前问题；重复、迟到和无效答复不能随意推进状态。")


def approval(d, s):
    d.paper(40,80,300,325,"已批准的操作",["接收人  甲", "草稿版本  v1", "操作  发送", "批准状态  " + ("已过期" if s==2 else "有效")])
    d.paper(662,80,300,325,"准备执行的操作",["接收人  " + ("乙" if s==1 else "甲"), "草稿版本  v1", "操作  发送"])
    if s==1:
        d.rect(680,144,265,41,"#f5dfd5",r=2);d.text(700,174,"接收人  乙",23,RED,650)
    d.line(355,240,443,240,GREEN if s==0 else RED,3,True)
    d.line(558,240,645,240,GREEN if s==0 else LINE,3,s==0)
    d.circle(500,240,56,GREEN if s==0 else RED,"none")
    if s==0:d.path("M474,238 l18,20 l35,-39",WHITE,5)
    else:d.path("M481,220 l38,40 M519,220 l-38,40",WHITE,5)
    d.text(500,333,["匹配并有效","参数已变化","批准已失效"][s],24,GREEN if s==0 else RED,650,"middle")
    d.text(500,443,"执行前再次核对当前权限、内容和有效期",22,d.muted,anchor="middle")
    d.note("获准执行，只是发送的前提；业务成功还要等实际结果。")


def sandbox(d, s):
    d.rect(195,48,630,397,"#e6ebe4",GREEN,10)
    d.text(225,91,"任务沙箱",29,GREEN,650)
    d.rect(252,130,226,168,WHITE,LINE,5);d.label(277,172,"检查脚本","仅处理当前草稿")
    d.rect(530,130,230,168,WHITE,LINE,5);d.label(555,172,"允许的文件","草稿 → 检查报告")
    d.line(479,235,518,235,GREEN,3,True)
    d.text(250,357,"文件 · 网络 · 进程 · 资源",26,weight=600)
    d.text(250,401,"每一面边界都要实际生效",22,d.muted)
    if s==1:
        d.path("M825,230 H910 V150",RED,3,True);d.line(849,208,884,253,RED,6);d.text(902,111,"外部资源",19,RED,anchor="middle")
    elif s==2:
        d.rect(224,321,571,101,"#f3dfd4",r=4);d.text(508,363,"资源超限 → 停止进程",28,RED,650,"middle");d.text(508,403,"收集诊断并清理临时资源",21,RED,anchor="middle")
    else:
        d.text(100,230,"其他文件",19,d.muted,anchor="middle");d.text(100,270,"默认不可读",18,d.muted,anchor="middle");d.line(157,250,185,250,LINE,3)
    d.note("示意边界，不代表容器默认具备这些限制；需要配置与越界验证。")


def extraction(d, s):
    d.text(45,62,"按时间看一串请求",29,weight=650)
    for i in range(6):
        x=90+i*130;y=160+(i%2)*73
        d.circle(x,y,31,d.accent if s else "#dbe7df","none")
        d.text(x,y+6,f"{i+1}",22,WHITE if s else GREEN,600,"middle")
        if i<5:d.line(x+34,y,x+96,160+((i+1)%2)*73,d.accent if s else LINE,2)
        d.text(x,300,"片段 " + chr(65+i) if s else "问题 "+str(i+1),19,d.muted,anchor="middle")
    if s:
        d.path("M88,328 V348 H745 V328",RED,3)
        d.text(425,395,"拼接后可能覆盖完整内容",28,RED,650,"middle")
    else:d.text(425,395,"授权范围内的独立问答",28,GREEN,650,"middle")
    d.rect(835,110,115,310,"#e9dfd5",r=6)
    for i,t in enumerate(["验证","限流","复核"]):d.text(892,180+i*82,t,22,RED if s==2 else d.muted,600,"middle")
    d.note("综合行为信号，分级处理；正常请求也必须进入评测，检查误伤。")


def trace(d, s):
    d.text(43,59,"TRACE / 一次任务",27,"#bdd3e2",650)
    for i,t in enumerate(["任务总览","模型判断","工具查询","再次查询","结果检查"]):d.text(45,140+i*65,t,22)
    for x in range(270,951,135):d.line(x,97,x,443,"#3b4b53",1,dash=True)
    bars=[(275,113,660),(275,178,155),(445,243,200),(655,308,170),(837,373,85)]
    if s==0:bars=[(275,113,660),(275,178,250),(540,243,280),(540,308,0),(837,373,85)]
    for i,(x,y,w) in enumerate(bars):
        if w:d.rect(x,y,w,33,["#4d666f","#8eb9d4",RED if s==1 else "#5e4039" if s==2 else "#8ab8a3","#5e4039" if s==2 else "#edb387","#a5b2df"][i],r=3)
    d.text(543,274,"超时" if s==1 else "成功" if s==0 else "缺成功证据",19,"#18272e" if s!=2 else "#efb4a1",600)
    if s==2:
        d.rect(530,238,300,42,"#3d3030",r=3);d.text(680,267,"没有成功查询记录",21,"#efb4a1",600,"middle")
    d.text(280,455,"开始",17,d.muted);d.text(930,455,"结束",17,d.muted,anchor="end")
    d.note("时间条为关系示意，无实测刻度。先定位哪一段出错，再谈优化。")


def evaluation(d, s):
    d.text(44,57,"同一组任务 · 相同条件",29,weight=650)
    d.text(570,119,"旧版本",24,weight=650,anchor="middle");d.text(820,119,"新版本",24,weight=650,anchor="middle")
    rows=[("正常查询",True,True),("负责人缺失",True,False),("工具超时",False,True),("权限拒绝",True,True)]
    for i,(t,a,b) in enumerate(rows):
        y=182+i*76;d.line(44,y+30,955,y+30);d.text(57,y,t,25)
        for x,val in [(570,a),(820,b)]:
            hidden=s==0 and i>0
            d.circle(x,y-8,19,LINE if hidden else GREEN if val else RED,"none")
            d.text(x,y-1,"?" if hidden else "✓" if val else "×",22,WHITE,600,"middle")
    if s==2:d.pill(45,427,"允许不同路径，检查必要约束",BLUE,480)
    d.note("此表是虚构演示结果。不要把顺利样本的通过，外推成整体提升。")


def plugin(d, s):
    d.rect(75,70,346,358,"#e4e8dc",r=8);d.text(105,113,"宿主应用",28,weight=650)
    for i,t in enumerate(["工具入口","Hooks","定时任务"]):
        y=155+i*80;d.rect(105,y,235,49,WHITE,LINE,3);d.text(124,y+32,t,23);d.rect(340,y+12,54,24,d.accent,r=2)
    d.rect(608,70,307,358,WHITE,LINE,8);d.text(638,113,"报告插件",28,weight=650)
    for i,t in enumerate(["查询工具","审计钩子","周报计划"]):
        y=179+i*80;d.text(645,y+7,t,23,d.muted);d.line(409,y,592,y,GREEN if s==0 else RED,3,s==0,s!=0)
    if s==1:d.pill(425,410,"在途调用 2",GOLD,190)
    if s==2:
        d.rect(624,212,275,182,"#f5e1d6",r=3);d.text(763,270,"初始化失败",26,RED,650,"middle");d.text(763,317,"回收已注册项",21,RED,anchor="middle");d.text(763,352,"关闭已建连接",21,RED,anchor="middle")
    d.note(["准备完成再开放能力，来源和版本可追踪。","拒绝新调用，排空已有工作，再断开资源。","安装失败也有清理路径，不能留下半套可见能力。"][s])


def hooks(d, s):
    d.text(50,67,"一次真实执行的两侧",29,weight=650)
    positions=[(160,250,"BEFORE","执行前"),(500,250,"TOOL","业务执行"),(840,250,"AFTER","执行后")]
    for x,y,t,sub in positions:
        d.rect(x-100,y-65,200,130,d.accent if t=="TOOL" else WHITE,LINE,6)
        d.text(x,y-8,t,22,WHITE if t=="TOOL" else d.ink,650,"middle",True)
        d.text(x,y+35,sub,26,WHITE if t=="TOOL" else d.ink,600,"middle")
    d.line(270,250,388,250,RED if s==0 else GOLD if s==2 else GREEN,4,s==1,s==2)
    d.line(610,250,728,250,GREEN if s==1 else LINE,4,True)
    if s==0:d.path("M316,222 L352,277 M352,222 L316,277",RED,5)
    d.text(160,143,"拦截不合法请求" if s==0 else "修改参数后重验" if s==2 else "检查通过",22,RED if s!=1 else GREEN,anchor="middle")
    d.text(840,143,"脱敏返回结果" if s==1 else "审计与整理",22,d.muted,anchor="middle")
    d.text(500,399,["拦住了，处理器不执行","动作已发生，事后检查不能自动撤销","最终参数才是实际执行的内容"][s],26,RED if s!=1 else GREEN,600,"middle")
    d.note("顺序、超时与失败策略要明确；必要授权仍需在可信执行入口落实。")


def terminal(d, s):
    for i,col in enumerate(["#d78978","#ddbe78","#80ab93"]):d.circle(63+i*27,43,7,col,"none")
    d.text(955,50,"demo / 仅作教学",17,d.muted,anchor="end",mono=True)
    if s==0:lines=[("$ demo-agent", "#b4d2ad"),("你 › 查询 TASK-01 的状态", "#f4f2e9"),("Agent › 已查询，任务目前受阻。", "#f4f2e9"),("你 › 为什么受阻？", "#f4f2e9"),("▌", "#b4d2ad")]
    elif s==1:lines=[("$ demo-agent -p '查询任务' --json", "#b4d2ad"),("stdout  →  {\"status\":\"blocked\"}", "#f4f2e9"),("stderr  →  查询完成 / 诊断信息", "#c3b8a5"),("exit    →  0", "#b4d2ad"),("下一段脚本只读取约定的结果", "#acb9bb")]
    else:lines=[("$ demo-agent", "#b4d2ad"),("执行工具中…", "#f4f2e9"),("^C", "#edb39a"),("停止新步骤，清理本地资源", "#f4f2e9"),("远端请求已发出，结果待核对", "#edb39a")]
    for i,(t,col) in enumerate(lines):d.text(54,132+i*64,t,25,col,mono=True)
    d.note("示意命令不是可安装产品；交互入口与单次自动化有不同约定。")


def schedule(d, s):
    d.text(45,62,"每周一 · 09:00",30,weight=650);d.text(955,61,"计划包含明确时区",19,d.muted,anchor="end")
    for i,t in enumerate(["周一","周二","周三","周四","周五"]):
        x=50+i*188;d.rect(x,102,168,132,WHITE,LINE,5);d.text(x+84,139,t,22,d.muted,anchor="middle");d.text(x+84,199,f"{12+i}",43,d.accent if i==0 else d.ink,650,"middle",True)
    d.line(133,249,133,307,d.accent,3,True)
    d.rect(52,326,340,100,"#e4e9db",r=5);d.text(76,364,"计划 S1 / 本次触发时点",22,weight=600);d.text(76,402,"稳定的运行身份",22,d.accent)
    d.line(408,376,549,376,RED if s==1 else d.accent,3,True)
    if s==1:
        d.path("M218,249 V290 H463 V351",RED,2,True,True);d.text(375,280,"重复提醒",18,RED,anchor="middle")
    d.paper(575,288,375,150,["创建任务实例","同一次运行，去重","上次未完，本次排队"][s],["随后跟踪执行与交付状态"])
    d.note("日期与时点仅为示意；错过触发、重叠和取消都需要明确规则。")


def journey(d, s):
    pts=[(95,176,"请求"),(290,176,"范围"),(500,176,"查询"),(700,176,"草稿"),(900,176,"验收")]
    d.text(47,61,"周报草稿的路线",30,weight=650)
    d.line(95,176,900,176,d.accent,8)
    for x,y,t in pts:d.circle(x,y,19,WHITE,d.accent,5);d.text(x,y-42,t,24,weight=600,anchor="middle")
    d.path("M290,195 V365 H500 V195",d.accent if s==1 else LINE,4,dash=s!=1)
    d.circle(393,365,18,WHITE,d.accent if s==1 else LINE,4);d.text(393,416,"澄清日期",23,d.accent if s==1 else d.muted,anchor="middle")
    d.path("M500,196 V282 H700 V196",RED if s==2 else LINE,4,dash=s!=2)
    d.text(600,321,"标记缺口",23,RED if s==2 else d.muted,anchor="middle")
    d.circle([900,393,600][s],[176,365,282][s],9,[GREEN,d.accent,RED][s],"none")
    d.paper(757,310,199,133,"到站产物",["有来源的草稿"])
    d.note("本任务不包含发送。每项机制在需要时接入，交付由完成标准验收。")


def identity(d, s):
    d.paper(54,80,358,340,"委托凭证 · 示意",["身份  当前用户", "动作  读取任务", "资源  自己的项目", "期限  当前任务"])
    d.rect(499,80,445,340,"#e5e8df",r=6);d.text(530,126,"业务服务的资源检查",27,weight=650)
    for i,t in enumerate(["可信身份","动作范围","资源归属","当前授权"]):
        y=189+i*57;fail=(s==1 and i==2)or(s==2 and i==3);d.circle(544,y-8,12,RED if fail else GREEN,"none");d.text(575,y,t+(("  已失效" if i==3 else "  不匹配") if fail else ""),23,RED if fail else d.ink)
    d.line(427,250,483,250,GREEN if s==0 else RED,3,True)
    d.note("模型参数不能自证身份；每次执行都使用可信授权与当前资源状态。")


def environment(d, s):
    d.text(45,57,"让项目能运行",29,weight=650);d.text(775,57,"让影响有边界",24,GREEN,650)
    layers=[(100,324,795,105,"隔离与资源边界",GREEN),(155,225,685,89,"运行时 · 依赖 · 测试替身",BLUE),(211,135,574,80,"仓库与本次任务文件",d.accent)]
    for i,(x,y,w,h,t,col) in enumerate(layers):
        unavailable=s==0 and i<2
        d.rect(x,y,w,h,"#e4e8df" if i==0 else WHITE,LINE,5)
        d.rect(x,y,8,h,LINE if unavailable else col)
        d.text(x+31,y+h/2+9,t,26,d.muted if unavailable else col,600)
        if unavailable:d.text(x+w-27,y+h/2+8,"缺失",22,RED,600,"end")
    if s==2:
        d.pill(632,149,"收集产物",GREEN,150)
        d.pill(676,246,"撤销授权",GREEN,150)
        d.pill(729,359,"回收实例",GREEN,150)
    d.note("环境定义可以复用；每次任务的临时状态、进程和凭证需要回收。")


RENDERERS = dict(enumerate([
    request, prompt, calling, react, mcp, skill, registry, memory, rag, wiki,
    routing, workflow, teamwork, subagent, a2a, runtime, events, clarification,
    approval, sandbox, extraction, trace, evaluation, plugin, hooks, terminal,
    schedule, journey, identity, environment,
], 1))
