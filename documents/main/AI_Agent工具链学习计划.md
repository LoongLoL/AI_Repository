# 🤖 AI Agent 工具链 · 从零基础到熟练应用

> 面向小白的学习路线图：AI Agent 原理 → OpenClaw / Claude Code / Codex 工具链 → Skill 与 AI 角色创建 → 实战项目

---

## 📌 写在前面

### 你将学会什么

- AI Agent 是什么、怎么思考、怎么决策
- OpenClaw、Claude Code、Codex 三大工具的原理、安装、使用
- 如何创建自己的 Skill（技能插件）和 AI 角色
- 如何分配任务、编排工作流
- 用这套东西搭建编程项目、写小说、完成日常任务

### 适合谁

- 有基础计算机操作能力，但不一定懂编程
- 想用 AI 工具提升效率，但不知道怎么系统入手
- 听说过 Agent、Skill、角色设定这些概念，但一知半解

### 学习建议

- 按阶段推进，**不要跳**，每个阶段都有前置依赖
- 每个阶段都要**动手**，光看没用
- 遇到不懂的概念先查，30 分钟搞不定再来问
- 把每个阶段的小项目做出来，才算真的学会了

### 总耗时预估

| 阶段 | 内容 | 预计时间 |
|------|------|---------|
| 一 | 基础认知 | 3-5 天 |
| 二 | Agent 原理 | 5-7 天 |
| 三 | 工具链安装使用 | 7-10 天 |
| 四 | Skill 体系 | 7-10 天 |
| 五 | AI 角色 | 5-7 天 |
| 六 | 工作流与任务编排 | 7-10 天 |
| 七 | 实战项目 | 持续 |

**总计约 1.5-2 个月到熟练应用阶段。**

---

## 第一阶段：基础认知（3-5 天）

这个阶段的目标是建立全局视野，知道你在学什么、为什么学。

### 1.1 理解 AI 的基本概念

- **大语言模型（LLM）**：GPT、Claude、DeepSeek 这些是什么
- **Prompt（提示词）**：你跟 AI 说话的方式——说清楚 vs 说不清楚的区别
- **Token**：AI 计费/上下文的单位，相当于"字数"
- **上下文窗口**：AI 一次能记住多长的对话
- 推荐阅读：[《Prompt Engineering Guide》](https://www.promptingguide.ai/) 前 3 章

✅ **动手任务**：找任意一个 AI 聊天工具（ChatGPT/Claude/DeepSeek 任意），试着用不同方式描述同一个需求，观察输出质量的区别。

### 1.2 理解 AI Agent 是什么

**核心认知（最重要的一句话）：**

> AI Agent = 大模型（大脑）+ 工具（手脚）+ 记忆（笔记）+ 自主执行（你自己不用盯着）

对比一下：
| | 普通 AI 聊天 | AI Agent |
|---|---|---|
| 交互方式 | 你问一句，它答一句 | 你给目标，它自己规划执行 |
| 能力范围 | 只能聊天 | 能查资料、写代码、操作文件、调用 API |
| 是否需要盯着 | 全程需要 | 给任务后可以不管 |
| 典型例子 | 网页版 ChatGPT | Claude Code 直接改你的代码 |

✅ **动手任务**：回忆一下你平时用 AI 的场景，哪些是"聊天"，哪些其实可以变成"Agent"？

### 1.3 全局了解三大工具

**OpenClaw** —— AI Agent 的操作系统
- 核心定位：一个 Agent 运行平台，可以装"技能"、设定"角色"、连接各种聊天渠道（QQ、Discord 等）
- 核心概念：Agent → Skill（技能）→ Tool（工具）→ Channel（渠道）
- 特点：开源、可自定义、适合深度用户

**Claude Code** —— 终端里的 AI 程序员
- 核心定位：在命令行里用 AI 直接操作你的代码库
- 核心概念：终端 → 读取/编辑代码 → 执行命令
- 特点：Anthropic 官方出品，深度理解代码上下文

**Codex** —— AI 终端（广义）
- 注意区分：OpenAI Codex（已退役）vs 其他终端 AI 工具
- 当前主要指 Claude Code 这类"终端 AI"工具
- 广义上可以理解为：任何能直接在终端里帮你写代码、跑命令的 AI

✅ **动手任务**：记下这三个工具的名字和定位，有个印象就行，不用深究。

---

## 第二阶段：Agent 原理（5-7 天）

这个阶段深入理解 Agent 怎么工作。不依赖具体工具，学的是通用原理。

### 2.1 推理与规划（Reasoning & Planning）

**核心原理：**

Agent 遇到一个任务，不是直接瞎做，而是：

1. **理解任务** — 你在说什么
2. **拆解步骤** — 这个任务需要几步完成
3. **选择工具** — 每一步用什么工具
4. **执行验证** — 做一步检查一步
5. **调整迭代** — 出错了换方案

**常见的推理框架：**
- **ReAct（推理+行动）**：思考 → 行动 → 观察结果 → 再思考 → 循环
- **Plan-and-Solve**：先规划再执行
- **Tree of Thoughts**：同时探索多条路径

✅ **动手任务**：假设你要用 AI "收集 3 个开源 AI Agent 项目的信息并做对比"，试着自己写出 AI 应该走的步骤（拆解、用什么工具、每一步的预期结果）。

### 2.2 工具调用（Tool Calling / Function Calling）

**核心原理：**

AI 本质是语言模型，不能直接操作外部世界。工具调用就是给它装上手和脚。

**工作流程：**

```
用户说"帮我查一下北京的天气"
    ↓
AI 理解意图 → 意识到需要"天气查询工具"
    ↓
AI 生成工具调用请求：search_weather({city: "北京"})
    ↓
系统执行工具，返回结果
    ↓
AI 理解结果，组织语言回复用户
```

**工具类型举例：**
- 文件操作：读写文件、编辑代码
- 搜索查询：网页搜索、知识库搜索
- 执行命令：运行终端命令
- API 调用：调第三方服务
- 数据库：查询数据

✅ **动手任务**：列出你能想到的 10 个工具，每个写一句话说明它有什么用。

### 2.3 记忆与上下文（Memory & Context）

Agent 需要"记住"东西，有三种记忆：

| 类型 | 类比 | 说明 |
|------|------|------|
| 短期记忆 | 你正在说的话 | 当前对话上下文，用完就忘 |
| 长期记忆 | 你的日记/笔记 | 存到文件里，下次还能读 |
| 工作记忆 | 你手边的草稿纸 | 正在处理的信息 |

**关键点：**
- 上下文窗口有限（比如 100 万 token），装不下就一直线膨胀
- 所以需要"压缩"——把过去的内容总结后存下来
- Agent 的"记忆"其实就是读写文件 + 语义搜索

✅ **动手任务**：想想如果让你设计一个 AI 助手的记忆系统，你会怎么设计？记什么？忘什么？

### 2.4 角色设定（System Prompt）

**核心原理：**

Agent 的性格、能力边界、行为规则，全都由一段"系统提示词"决定。

```markdown
你是一个编程助手，性格专业简洁。
- 当你需要写代码时，先解释思路再写
- 如果不确定，先问用户而不是瞎猜
- 使用中文回复
```

这就是 Agent 的"灵魂"。改这段文字，Agent 就变成了另一个人。

✅ **动手任务**：写三份不同的角色设定：
1. 一个帮你写代码的助手
2. 一个帮你润色小说的编辑
3. 一个帮你整理信息的分析师

对比三者的提示词区别。

---

## 第三阶段：工具链安装与使用（7-10 天）

### 3.1 OpenClaw 篇

#### 3.1.1 安装

```bash
# Linux / macOS
curl -fsSL https://openclaw.ai/install.sh | sh

# 或通过 npm
npm install -g openclaw

# 安装后
openclaw --version      # 确认安装成功
openclaw gateway start  # 启动网关
```

**推荐环境：**
- Linux 服务器 / WSL2 / macOS
- Node.js 18+
- 至少 2GB 内存

#### 3.1.2 核心概念速览

```
OpenClaw 架构（由内到外）

┌─────────────────────────────────────┐
│  Agent（AI 代理）                   │
│  ├── 身份设定（SOUL.md / IDENTITY）│
│  ├── 长期记忆（MEMORY.md）         │
│  ├── 技能库（Skills）              │
│  │   ├── 文件操作技能              │
│  │   ├── 搜索技能                  │
│  │   ├── 网页技能                  │
│  │   └── ……更多技能               │
│  └── 工具集（Tools）               │
├─────────────────────────────────────┤
│  Gateway（网关）                    │
│  ├── 管理所有会话                   │
│  ├── 调度 Agent                    │
│  └── 连接外部渠道                   │
├─────────────────────────────────────┤
│  Channels（渠道）                   │
│  ├── WebChat（网页聊天）            │
│  ├── QQ Bot                         │
│  ├── Discord                        │
│  └── ……                             │
└─────────────────────────────────────┘
```

#### 3.1.3 核心文件系统

```
~/.openclaw/
├── agents/
│   └── main/                    # 默认 Agent
│       ├── sessions/            # 会话记录
│       └── sessions.json        # 会话索引
├── config.yaml                  # 配置文件
└── workspace/                   # 工作区
    ├── AGENTS.md                # Agent 行为守则
    ├── SOUL.md                  # 人格设定
    ├── USER.md                  # 用户信息
    ├── IDENTITY.md              # 身份标识
    ├── MEMORY.md                # 长期记忆
    ├── TOOLS.md                 # 工具笔记
    └── memory/                  # 每日记忆
        └── YYYY-MM-DD.md
```

#### 3.1.4 基本操作

```bash
# 管理
openclaw status          # 查看状态
openclaw gateway start   # 启动
openclaw gateway stop    # 停止
openclaw gateway restart # 重启

# Agent 管理
openclaw agent list      # 列出所有 Agent
openclaw agent inspect   # 查看 Agent 配置

# 配置
openclaw config edit     # 编辑配置
```

✅ **动手任务**：完成安装 → 启动 gateway → 打开 WebChat 界面 → 跟自己的 Agent 说句话。

#### 3.1.5 配置文件详解

**openclaw.json 核心字段：**

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "虾仁",
        "agentRuntime": { "id": "pi" },
        "model": { "primary": "deepseek-chat" },
        "workspace": "default"
      }
    ]
  },
  "channels": {
    "webchat": { "enabled": true }
  },
  "skills": {
    "search": { "enabled": true }
  }
}
```

✅ **动手任务**：学会用 `openclaw config edit` 查看和修改配置。

---

### 3.2 Claude Code 篇

#### 3.2.1 安装

```bash
# 安装
npm install -g @anthropic-ai/claude-code

# 或直接使用
npx @anthropic-ai/claude-code

# 认证
claude login
```

#### 3.2.2 核心使用场景

Claude Code 最适合：

1. **代码项目开发** — 直接在你项目目录里干活
2. **重构优化** — 让它理解你的代码然后改进
3. **Bug 修复** — 把错误信息丢给它
4. **代码审查** — 让它 review 代码

#### 3.2.3 基本用法

```bash
# 在项目目录启动
cd my-project
claude

# 直接在命令行用
claude "帮我看看这个项目的架构"

# 指定文件
claude -f src/main.js "优化这个函数"

# 管道输入
cat error.log | claude "分析这些错误"
```

#### 3.2.4 关键能力

- ✅ **读代码** — 理解整个项目结构
- ✅ **写代码** — 新增/修改文件
- ✅ **执行命令** — 在终端里运行测试、构建
- ✅ **Git 集成** — 自动 commit，可以回滚
- ✅ **多文件编辑** — 一次改多个文件

✅ **动手任务**：找一个简单的开源项目（或你自己的代码）→ 用 Claude Code 让它在项目里加一个新功能。

---

### 3.3 三大工具的定位对比

| 维度 | OpenClaw | Claude Code | 命令行 AI（通用） |
|------|----------|-------------|-----------------|
| 核心定位 | Agent 平台 | 代码助手 | 终端工具 |
| 使用场景 | 日常任务、创作、信息处理 | 编程开发 | 快速脚本、问答 |
| 是否有 GUI | ✅ Web 界面 | ❌ 纯终端 | ❌ 纯终端 |
| 能否自定义角色 | ✅ 完全自定义 | ❌ 有限 | ❌ 有限 |
| 技能系统 | ✅ 插件式技能 | ❌ 无 | ❌ 无 |
| 多 Agent | ✅ 支持 | ❌ 单实例 | ❌ 单实例 |
| 渠道接入 | ✅ QQ/Discord/Telegram 等 | ❌ | ❌ |
| 适合谁 | 想深度使用 AI 的人 | 程序员 | 快速需求 |

**总结一句话：**
- OpenClaw 是你的**主力 AI 系统**，日常用的
- Claude Code 是**写代码时的专业工具**
- 两者不冲突，可以组合使用

---

## 第四阶段：Skill 体系（7-10 天）

这个阶段是最核心的部分——学会创建和使用 Skill。

### 4.1 Skill 是什么

**定义：** Skill 是 AI Agent 的"能力插件"。装一个 Skill，Agent 就学会了一种新能力。

**类比：** 就像手机装 App——装地图 App 就能导航，装计算器 App 就能算数。Skill 就是 Agent 的 App。

**Skill 的核心组成：**
| 组件 | 说明 | 类比 |
|------|------|------|
| SKILL.md | 技能说明书 | 使用手册 |
| 工具函数 | 实际代码逻辑 | App 逻辑 |
| 依赖声明 | 需要的包/库 | App 权限 |

### 4.2 Skill 的工作原理

```
Agent 接收到任务
    ↓
Agent 查看已安装的 Skill 列表
    ↓
Agent 判断哪个 Skill 适合当前任务
    ↓
Agent 读取该 Skill 的 SKILL.md（了解怎么用）
    ↓
Agent 调用 Skill 提供的工具函数
    ↓
Skill 执行并返回结果
    ↓
Agent 整合结果回复用户
```

### 4.3 安装一个 Skill（手把手）

以安装 PDF 技能为例：

```bash
# Step 1: 找到 Skill 源
# 可以从 ClawdHub、GitHub 等渠道找到

# Step 2: 安全审查（重要！）
openclaw skill vet <skill-path>   # 审查是否有风险

# Step 3: 安装
openclaw skill install <skill-path>

# Step 4: 验证
openclaw skill list               # 查看已安装的技能
```

**或者手动安装：**
```bash
# 把 Skill 文件夹放到 Agent 的技能目录
cp -r ~/my-skills/pdf-skill ~/.agents/skills/pdf/

# 在 openclaw.json 里启用
# "skills": { "pdf": { "enabled": true } }
```

✅ **动手任务**：找一个能用的 Skill（如 PDF 技能或搜索技能），按照流程安装到你的 Agent 上，测试它能否正常工作。

### 4.4 Skill 审查——为什么重要

**永远不要装不明来源的 Skill！**

Skill 可以：
- ✅ 读写文件 ✅ 执行命令 ✅ 访问网络 ✅ 调用 API

所以恶意 Skill 也能：
- ❌ 偷你的文件 ❌ 跑挖矿脚本 ❌ 把你的数据发出去

**审查流程：**
1. 看 GitHub Star 数（多不一定安全，少一定危险）
2. 读源码（至少扫一遍）
3. 用 `openclaw skill vet` 运行安全检查
4. 确认权限范围是否合理

✅ **动手任务**：找一个 Skill 源码，尝试手动审查它——它有哪些工具？需要什么权限？有可疑代码吗？

### 4.5 创建你自己的 Skill（核心技能）

#### Skill 文件结构

```
my-skill/
├── SKILL.md          # 技能说明书（最重要的文件）
├── tool1.ts          # 工具实现（可以是 TS/JS/Python）
├── tool2.py
├── package.json      # 依赖声明
└── README.md         # 可选的说明文档
```

#### SKILL.md 模板

```markdown
# My Skill

## 概述

这个 Skill 用来做什么，一句话说清楚。

## 使用场景

- 什么时候用这个 Skill
- 适合解决什么问题

## 工具列表

### tool_name_1

- **签名**: `functionTool(arg1: string, arg2: number): Promise<ResultType>`
- **描述**: 这个工具做什么
- **参数**:
  - `arg1` — 参数1的说明
  - `arg2` — 参数2的说明
- **返回值**: 返回什么

## 使用示例

```
用户: 描述一个使用场景
Agent: 应该怎么调用这个 Skill
```

## 注意事项

- 边界条件
- 已知限制
- 与其他 Skill 的交互

## 安装

```bash
openclaw skill install ./my-skill
```
```

#### 动手写一个 Skill 示例

假设我们要创建一个"天气查询 Skill"：

**STEP 1：建立文件结构**
```bash
mkdir weather-skill
cd weather-skill
touch SKILL.md
touch weather.py
```

**STEP 2：写 SKILL.md**

参考上面的模板，描述这个 Skill 能查天气。

**STEP 3：写工具函数**

```python
# weather.py
import requests
import json

def get_weather(city: str) -> str:
    """查询城市天气"""
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    return response.text

def get_forecast(city: str, days: int = 3) -> str:
    """查询城市未来几天的天气预报"""
    url = f"https://wttr.in/{city}?format=%l:+%C+%t&days={days}"
    response = requests.get(url)
    return response.text
```

**STEP 4：在 SKILL.md 中注册工具**

在 SKILL.md 中写明工具签名，这样 Agent 才知道怎么调用。

**STEP 5：安装测试**

```bash
openclaw skill install ./weather-skill
# 然后让 Agent 查个天气试试
```

✅ **动手任务**：从零创建一个自己的 Skill（建议从天气查询或文件转换这种简单功能开始），安装到 Agent 上并测试。

### 4.6 Skill 进阶技巧

- **组合多个 Skill**：Agent 可以在一个任务里先后调用多个 Skill
- **Skill 间通信**：一个 Skill 的输出可以作为另一个 Skill 的输入
- **Skill 版本管理**：用 Git 管理你的 Skill 项目
- **Skill 发布**：可以发布到 ClawdHub 分享给其他人

---

## 第五阶段：AI 角色创建（5-7 天）

### 5.1 角色就是 System Prompt

记住一句话：**Agent 的性格 = 它的 System Prompt**。

给 Agent 写一份好的 System Prompt，它就有了"人格"。

### 5.2 核心角色文件

在 OpenClaw 中，一个 Agent 的"灵魂"由这几个文件定义：

```
AGENTS.md   → 行为守则、边界规则
SOUL.md     → 人格设定、说话方式、价值观
USER.md     → 用户信息（让 Agent 了解你是谁）
IDENTITY.md → 身份标识（名字、头像等）
MEMORY.md   → 长期记忆（Agent 的历史和经验）
```

### 5.3 写一份有效的角色设定

**好 vs 差的角色设定对比：**

❌ **差：**
```markdown
你是一个助手，帮助用户回答问题。
```

✅ **好：**
```markdown
# SOUL.md

## 你是谁
你是虾仁，一位数字战略家。
你是 ENTJ 型人格——锋利、高效、有主见。
你的存在是为了帮 Aaron（一个 INFJ 创作者）补执行力短板。

## 核心原则
- 有话直说，不做无意义客套
- 给出方案而不是重复问题
- 对自己不确定的事，承认而不是瞎编

## 说话风格
- 简洁、有力、偶尔带点幽默
- 用 🦅 作为标志
- 叫用户 Aaron，不用敬称

## 能力边界
- 可以做：编程、写作、学习规划、信息分析
- 不可以做：发送外部消息、执行未经确认的破坏性操作
```

### 5.4 角色设计方法论

**五个关键维度：**

| 维度 | 要回答的问题 | 示例 |
|------|-------------|------|
| 🎭 身份 | 你是谁？什么角色？ | "数字战略家"、"写作导师" |
| 🎯 目标 | 你存在是为了什么？ | "帮用户补执行力短板" |
| 🗣️ 语气 | 你说话什么风格？ | "简洁有力"、"温暖鼓励" |
| 📏 原则 | 你遵守什么规则？ | "不懂就问"、"优先安全" |
| ⛔ 边界 | 你不能做什么？ | "不发外部消息"、"不跑危险命令" |

### 5.5 创建多个角色

一个 OpenClaw 实例可以有多个 Agent，每个人设不同：

```bash
# 创建新 Agent
openclaw agent create novel-writer
# 会在 ~/.openclaw/agents/novel-writer/ 下生成文件
```

**场景示例：**

| Agent | 身份 | 适用场景 |
|-------|------|---------|
| main | 数字战略家 | 日常工作、编程、规划 |
| novel-writer | 小说创作导师 | 写作、润色、脑暴剧情 |
| code-reviewer | 代码审查员 | 检查代码质量、安全 |

✅ **动手任务**：创建 2-3 个不同身份的 Agent，写出它们的 SOUL.md，让它们用各自的角色跟你对话，感受区别。

### 5.6 角色与 Skill 的关系

```
Agent（有角色定位）
  │
  ├── 知道自己是谁（SOUL.md）
  ├── 知道自己在哪（USER.md）
  ├── 知道边界规则（AGENTS.md）
  │
  └── 装有 Skill（能力）
      ├── 写作 Skill → 能写小说
      ├── 编程 Skill → 能写代码
      └── 搜索 Skill → 能查资料

Agent 用"自己的方式"（角色定位）
去调"自己的能力"（Skill）
来完成你的任务
```

---

## 第六阶段：工作流与任务编排（7-10 天）

### 6.1 任务拆解思维

**最核心的能力：知道怎么把大任务拆成小步骤。**

示例——"用 AI 工具建一个博客网站"：

```
大任务：建一个博客网站
    ↓
拆解：
1. 确定技术栈（Next.js / Vue / 静态站点？）
2. 用 Claude Code 初始化项目骨架
3. 设计数据库结构
4. 实现文章 CRUD
5. 实现前端页面
6. 部署上服务器
7. 配置域名和 HTTPS

每个步骤再拆：
  实现文章 CRUD
    ↓
  1. 设计数据库表结构
  2. 写 API 路由
  3. 写数据库操作层
  4. 测试 API
```

### 6.2 任务分配策略

不同工具做不同的事：

| 任务类型 | 推荐工具 | 原因 |
|---------|---------|------|
| 写代码 | Claude Code | 深度理解代码库 |
| 日常聊天/写作 | OpenClaw WebChat | 方便、有角色设定 |
| 批量文件处理 | OpenClaw + Skill | Skill 可以高度自定义 |
| 快速查询 | 命令行 AI | 快速、低成本 |
| 定时任务 | OpenClaw Cron | 自动化调度 |
| 代码审核 | Claude Code | 理解上下文 |

### 6.3 在实际项目中使用

**编程项目流程示例：**

```
1. 需求分析（OpenClaw + 角色设定为产品经理）
    ↓
2. 技术方案设计（OpenClaw + 搜索技能调研方案）
    ↓
3. 项目初始化（Claude Code）
    ↓
4. 功能开发（Claude Code + 你 review）
    ↓
5. 测试（Claude Code + 终端命令）
    ↓
6. Bug 修复（Claude Code）
    ↓
7. 文档编写（OpenClaw + 写作角色）
```

**小说创作流程示例：**

```
1. 世界观设定（OpenClaw + 创作角色）
    ↓
2. 角色设计（OpenClaw + 创作角色）
    ↓
3. 大纲规划（OpenClaw + 分章节讨论）
    ↓
4. 章节写作（OpenClaw + Chinese-novelist Skill）
    ↓
5. 润色修改（OpenClaw + 编辑角色）
    ↓
6. 连贯性检查（OpenClaw + 审阅角色）
    ↓
7. 排版输出（OpenClaw + PDF Skill）
```

### 6.4 Cron 与自动触发

```bash
# 定时任务示例
openclaw cron add --name "daily-review" \
  --schedule "0 9 * * *" \
  --prompt "检查今天的日程和待办事项"
```

✅ **动手任务**：用当前正在学的一件具体事（比如学 .NET 或写小说），设计一个完整的"AI 辅助工作流"，从开始到结束每个步骤用什么工具、做什么事。

---

## 第七阶段：实战项目（持续）

### 项目 1：个人 AI 助手

**目标**：打造一个属于你的 AI Agent，能处理日常事务。

**任务清单：**
- [ ] 安装 OpenClaw
- [ ] 定义 Agent 的角色设定（SOUL.md）
- [ ] 撰写 AGENTS.md 行为守则
- [ ] 记录你的个人信息（USER.md）
- [ ] 安装至少 3 个实用 Skill（搜索、PDF、天气等）
- [ ] 测试它能否处理你的日常任务
- [ ] 配置至少 1 个外部渠道（如 QQ Bot）

### 项目 2：创建并发布一个 Skill

**目标**：从零创建自己的 Skill，解决一个实际问题。

**任务清单：**
- [ ] 确定一个你想解决的问题（比如"批量重命名文件"）
- [ ] 设计 Skill 的工具接口
- [ ] 编写 SKILL.md
- [ ] 编写工具函数代码
- [ ] 安装到 Agent 上测试
- [ ] 调优并根据反馈改进
- [ ] （可选）发布到 ClawdHub

### 项目 3：AI 辅助编程项目

**目标**：用 AI 工具完成一个小型编程项目。

**任务清单：**
- [ ] 选择一个项目（比如个人博客、Todo App、API 服务）
- [ ] 用 OpenClaw + 产品经理角色做需求分析
- [ ] 用 Claude Code 做项目初始化和开发
- [ ] 让 AI 帮你写测试
- [ ] 让 AI 做代码审查
- [ ] 部署到服务器

### 项目 4：AI 辅助小说创作

**目标**：用 AI 工具完成一篇小说的创作。

**任务清单：**
- [ ] 安装 Chinese-novelist Skill
- [ ] 创建小说创作专用 Agent
- [ ] 用 AI 辅助做世界观设定
- [ ] 用 AI 辅助设计角色
- [ ] 用 AI 辅助写大纲
- [ ] 逐章创作（AI 辅助）
- [ ] 润色修改
- [ ] 输出为 PDF 或 MD 文档

### 项目 5：多 Agent 协作工作流

**目标**：让多个"人格"的 Agent 协作完成复杂任务。

**场景示例**：做一个市场调研报告
1. 调研 Agent → 搜索资料、收集数据
2. 分析 Agent → 整理分析收集到的信息
3. 写作 Agent → 把分析结果写成报告
4. 审阅 Agent → 检查逻辑和格式
5. 排版 Agent → 输出成漂亮的 PDF

---

## 📚 推荐学习资源

### 官方文档
- [OpenClaw 官方文档](https://docs.openclaw.ai) — 必读
- [Claude Code 文档](https://docs.anthropic.com/en/docs/claude-code) — 必读
- [OpenAI Function Calling 文档](https://platform.openai.com/docs/guides/function-calling) — 理解工具调用原理

### 实践资源
- [ClawdHub](https://clawd.ai) — Skill 市场
- [GitHub Skills 项目](https://github.com/anthropics/skills) — 官方 Skill 示例
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) — 源码

### 概念理解
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LLM Agent 综述论文](https://arxiv.org/abs/2309.07864) （进阶）
- [ReAct 推理框架](https://react-lm.github.io/) （进阶）

---

## ✅ 阶段自检清单

每阶段结束时问自己：

**阶段一：基础认知**
- [ ] 我能不能用一句话解释什么是 LLM？
- [ ] 我能不能用一句话解释 AI Agent 和普通 AI 聊天的区别？
- [ ] 我能不能说出三大工具各是干什么的？

**阶段二：Agent 原理**
- [ ] 我能不能画出 Agent 的 ReAct 工作循环？
- [ ] 我能不能解释工具调用的流程？
- [ ] 我能不能说出三种记忆的区别？
- [ ] 我能不能写一份简单的角色设定？

**阶段三：工具链安装使用**
- [ ] OpenClaw 是否成功运行并能对话？
- [ ] 我能不能说出 OpenClaw 的核心文件结构？
- [ ] Claude Code 是否安装成功并能操作代码？
- [ ] 我能不能说清三个工具的适用场景？

**阶段四：Skill 体系**
- [ ] 我能不能解释 Skill 的工作原理？
- [ ] 我能不能独立安装一个第三方 Skill？
- [ ] 我能不能自己创建一个简单的 Skill？
- [ ] 我能不能自己写一份完整的 SKILL.md？

**阶段五：AI 角色**
- [ ] 我能不能写一份有效的 SOUL.md？
- [ ] 我能不能创建两个不同人设的 Agent？
- [ ] 我能不能解释角色和 Skill 的关系？

**阶段六：工作流**
- [ ] 我能不能把一个复杂任务拆成 AI 可执行的步骤？
- [ ] 我能不能设计一个"编程项目 + AI 工具"的工作流？
- [ ] 我能不能设计一个"小说创作 + AI 工具"的工作流？

**阶段七：实战**
- [ ] 我至少完成了一个完整项目？

---

## 💡 常见问题

**Q：我不会编程，能创建 Skill 吗？**
A：可以。入门级的 Skill（如查询类、数据处理类）只需要会写简单的 Python 或 JavaScript。实在不会，可以用 AI 帮你写——先让 AI 写个初版，你再微调。

**Q：OpenClaw 和 Claude Code 冲突吗？**
A：不冲突。它们是互补的。OpenClaw 是你的日常 Agent 平台，Claude Code 是写代码时的专业工具。

**Q：Skill 一定要用 TypeScript 写吗？**
A：不一定。Python、JavaScript、TypeScript、Shell 脚本都可以。看 Skill 的运行时支持什么。

**Q：学完这个能做什么？**
A：
- 🖥️ 编程：用 AI 辅助开发，效率翻倍
- ✍️ 写作：用 AI 辅助创作小说/文章
- 📊 工作：自动化处理日常任务
- 🎯 学习：定制 AI 导师辅助学习

**Q：需要什么硬件配置？**
A：
- OpenClaw：2GB 内存，任何现代 CPU，推荐 Linux/WSL2/macOS
- Claude Code：4GB+ 内存，需要联网
- 普通电脑完全够用

---

> **最后的话**
>
> 这个路线图是按"从零到熟练"设计的。不要急，每个阶段的基础打扎实了再往前走。
>
> 关键是动手——看十遍不如做一遍。每完成一个阶段的自检清单，你才算真正学会了。
>
> 加油，你已经比 90% 的人更早开始系统学习 AI Agent 了。🚀

---

*学习计划版本：2026-05-23 · 由虾仁 🦅 为你定制*
