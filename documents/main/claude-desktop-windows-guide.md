# Claude Desktop Windows 完全使用指南（2026版）

> 一切以**免费使用**为主，涵盖安装 → 配置 → MCP → Skills → 日常使用的完整流程。

---

## 一、下载与安装

### 1.1 系统要求

- Windows 10/11（64位）
- 内存 ≥ 8GB（推荐 16GB）
- 需要能访问 claude.ai（可能需要代理）

### 1.2 下载安装

**官方下载地址：** <https://claude.com/download>

1. 进入官网 → 选择 **Windows** 版本下载
2. 运行安装程序，按提示完成安装
3. 启动后用 Anthropic 账号登录（免费账号即可使用）

### 1.3 账号说明

| 方案 | 费用 | 说明 |
|------|------|------|
| **免费账号** | ¥0 | 有用量限制，适合日常轻度使用 |
| Pro 订阅 | ~$20/月 | 更高用量 + Claude Code 功能 |
| Max 订阅 | ~$200/月 | 超大用量，适合重度开发者 |

**免费账号已经可以使用 Claude Desktop 的大部分功能**，包括 Skills、MCP 等。

---

## 二、核心概念

Claude Desktop 有三大扩展体系：

| 概念 | 是什么 | 类比 |
|------|--------|------|
| **Skills（技能包）** | 告诉 Claude "怎么做某件事"的指令集 | 工作手册 |
| **MCP Servers（模型上下文协议）** | 让 Claude 能连接外部工具和数据的协议 | USB-C 转接器 |
| **Desktop Extensions（桌面扩展）** | 一键安装的 MCP 服务器打包格式（.mcpb） | App Store |

---

## 三、Skills（技能包）— 免费安装与使用

### 3.1 Skills 是什么？

Skills 是一个包含 `SKILL.md` 文件的文件夹，告诉 Claude 如何执行特定任务。**2026 年已开放给免费用户使用。**

核心特点：
- **渐进式披露** — 只在需要时加载，不浪费上下文窗口
- **一次设置，反复使用** — Claude 自动识别并调用

### 3.2 内置 Skills（免费自带）

Claude Desktop/Claude Code 自带多个内置技能：

| Skill | 功能 |
|-------|------|
| `commit` | Git commit 规范化 |
| `review-pr` | PR 代码审查 |
| `frontend-design` | 前端设计辅助 |
| `doc-coauthoring` | 文档协作撰写 |
| `canvas-design` | Canvas 设计 |
| `pdf` | PDF 处理 |
| `algorithmic-art` |算法艺术生成 |

### 3.3 安装自定义 Skills（免费方法）

#### 方法一：手动安装（推荐，完全免费）

```powershell
# 1. 创建 Skills 目录（如果不存在）
mkdir -p %USERPROFILE%\.claude\skills

# 2. 将下载的 Skill 文件夹放入该目录
# 结构：~/.claude/skills/SKILL_NAME/SKILL.md
```

#### 方法二：通过 Skill Creator 创建自己的 Skill

直接告诉 Claude：
```
"我想创建一个 Skill，功能是 [你的需求]"
```
Skill Creator 会引导你一步步创建。

#### 方法三：从 GitHub 社区获取免费 Skills

推荐资源：
- **Anthropic 官方**: <https://github.com/anthropics/claude-code>
- **Superpowers 系列**: <https://github.com/obra/superpowers>（开发工作流，中文社区有汉化版）
- **awesome-openclaw-skills**: <https://github.com/VoltAgent/awesome-openclaw-skills>（5400+ 技能）

### 3.4 Skills 使用技巧

开启 Skills 的方法：
1. 打开 Claude Desktop
2. Settings → Capabilities → 确保 Skills 已启用
3. 对话时直接描述需求，Claude 自动匹配对应 Skill

```
✅ "帮我创建一个 git commit"    → 自动调用 commit skill
✅ "审查这个 PR"                → 自动调用 review-pr skill
✅ "帮我设计一个前端页面"        → 自动调用 frontend-design skill
```

**自定义 Skills 存放路径：**

| 范围 | 路径 |
|------|------|
| 全局（个人） | `%USERPROFILE%\.claude\skills\` |
| 项目级 | 项目根目录 `.claude\skills\` |

---

## 四、MCP Servers — 免费安装与配置

### 4.1 MCP 是什么？

**Model Context Protocol（模型上下文协议）**，Anthropic 推出的开放标准，让 AI 能安全地连接外部工具和数据源。

```
没有 MCP 的 Claude  ≈ 一台没有连网的电脑
配置 MCP 后的 Claude  ≈ 能操控一切的外脑
```

### 4.2 前置条件

- **Node.js 18+**（必须）：<https://nodejs.org> 下载 LTS 版
- Claude Desktop 最新版

验证安装：
```powershell
node --version   # 应显示 v18.x 或更高
npx --version    # 应正常显示版本
```

### 4.3 配置文件位置

```
Windows: %APPDATA%\Claude\claude_desktop_config.json
即：C:\Users\你的用户名\AppData\Roaming\Claude\claude_desktop_config.json
```

**打开配置的三种方式：**

1. **方式A（推荐）**：Claude Desktop → File → Settings → Developer → Edit Config
2. **方式B**：用记事本打开上述路径的 JSON 文件
3. **方式C**：通过 Claude Code CLI 命令添加

### 4.4 免费 MCP 服务器推荐

#### 🏆 必装（全部免费）

**① Filesystem（文件系统）— 文件读写**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\你的用户名\\Desktop",
        "C:\\Users\\你的用户名\\Downloads",
        "C:\\Users\\你的用户名\\Documents"
      ]
    }
  }
}
```

> ⚠️ Windows 路径注意：使用 `\\` 或 `/`，不要用单个 `\`

**效果**：Claude 可以直接读写你指定的文件夹 → "帮我把下载的文件按类型整理一下"

---

**② Fetch（网页抓取）— 读取网页内容**
```json
{
  "mcpServers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@kazuph/mcp-fetch"]
    }
  }
}
```

> 完全免费，无需 API Key

**效果**："帮我总结这篇文章 https://example.com"

---

**③ Memory（记忆管理）— 持久记忆**
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

> 完全免费！让 Claude 跨会话记住重要信息

**效果**：Claude 能记住你的偏好、项目上下文、历史决策

---

**④ Sequential Thinking（思维链）— 复杂推理**
```json
{
  "mcpServers": {
    "thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

> 免费。提升 Claude 解决复杂问题的能力

---

**⑤ Context7（文档查询）— 查库文档**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

> 免费！接入 Upstash Context7 库文档，查任何编程库的最新文档

---

#### 🔧 可选免费 / 有免费额度

**⑥ Brave Search（网页搜索）**
- **免费额度**：2000 次/月
- 申请 API Key：<https://brave.com/search/api/>（注册 → 创建密钥 → 选 Free 套餐）

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "你的API密钥"
      }
    }
  }
}
```

**效果**：Claude 能实时搜索网页，获取最新资讯

---

**⑦ GitHub（代码仓库管理）**
- **免费**：不需要 API Token（公开仓库）
- **私有仓库**：需要 GitHub Personal Access Token（免费生成）

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

> GitHub Token 生成：GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

---

#### 🚫 已移除 / 不再推荐

| MCP | 原因 |
|-----|------|
| **Firecrawl** | 需要付费 API，DNS 经常不可达 |
| **某些付费数据源** | 不符合免费为主的定位 |

### 4.5 完整配置示例

将以下内容写入 `claude_desktop_config.json`（**替换路径中的用户名**）：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\你的用户名\\Desktop",
        "C:\\Users\\你的用户名\\Documents",
        "C:\\Users\\你的用户名\\Downloads"
      ]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@kazuph/mcp-fetch"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "BSA-XXXXXXXXXXXXXXXXX"
      }
    }
  }
}
```

### 4.6 Windows 常见故障排除

| 问题 | 解决方案 |
|------|----------|
| 🔨 锤子图标不出现 | 检查 JSON 格式是否正确；重启 Claude |
| 路径错误 `'C:\Program' is not recognized` | 用全路径 `C:\\Program Files\\nodejs\\npx.exe` |
| `${APPDATA}` 未展开 | 在 env 中添加 `"APPDATA": "C:\\Users\\user\\AppData\\Roaming\\"` |
| npx 命令失败 | 全局安装：`npm install -g npx`；或用 nvm 管理 Node |
| 中文路径问题 | 避免在允许的目录中使用中文路径 |
| 调试日志 | 查看 `%APPDATA%\Claude\logs\mcp*.log` |

---

## 五、Desktop Extensions（桌面扩展 / .mcpb）

### 5.1 什么是 .mcpb？

Anthropic 2025 年推出的**一键安装格式**，将 MCP 服务器打包成 `.mcpb` 文件，像安装 App 一样简单。

### 5.2 扩展资源（免费）

| 来源 | 说明 |
|------|------|
| <https://claude.com/plugins> | 官方插件市场 |
| <https://github.com/punkpeye/awesome-mcp-servers> | 社区汇总（88K stars） |
| <https://github.com/danielrosehill/Claude-Code-MCP-List> | 27 stars 精选列表 |
| <https://mcp.so> | MCP 搜索引擎 |

### 5.3 安装方法

1. 下载 `.mcpb` 文件
2. 双击文件 → 自动在 Claude Desktop 中安装
3. 或在 Claude Desktop 中：Settings → Extensions → Install Extension

---

## 六、Claude Code（桌面版内置）

### 6.1 什么是 Claude Code？

Anthropic 推出的**终端 AI 编程 Agent**，已集成到 Claude Desktop 桌面版中。

- **免费版**：有限用量，适合轻度开发
- **Pro 订阅**：更高用量 + 更多模型选择

### 6.2 在 Windows 上安装 Claude Code CLI

```powershell
# 方法一：PowerShell 一键安装（推荐）
irm https://claude.ai/install.ps1 | iex

# 验证安装
claude --version
```

**前置要求：**
- Node.js 18+
- Git for Windows（推荐，提供 Git Bash 环境）

### 6.3 Claude Code 在桌面版中的使用

1. 打开 Claude Desktop
2. 新建会话 → 选择 **Local Session**（本地会话）
3. 选择项目文件夹
4. Claude Code 会自动分析项目结构并可以执行代码任务

---

## 七、日常使用技巧

### 7.1 项目级配置

在项目根目录创建 CLAUDE.md / .claude/ 文件夹，Claude 每次启动会自动加载：

```
📁 my-project/
├── 📁 .claude/
│   ├── 📄 CLAUDE.md          # 项目说明
│   ├── 📁 skills/             # 项目专属 Skills
│   └── 📁 commands/           # 快捷命令
└── 📁 src/
```

**CLAUDE.md 示例：**
```markdown
# 项目说明
这是一个 .NET Web API 项目，使用 C# 12 + .NET 8

## 编码规范
- 使用 PascalCase 命名方法
- 每个类放在独立文件中
- 使用 async/await 处理异步操作

## 常用命令
- 构建: dotnet build
- 测试: dotnet test
- 运行: dotnet run --project src/Api
```

### 7.2 日常高效用法

| 场景 | 操作 |
|------|------|
| **帮整理文件** | "帮我把 Desktop 上的文件按类型分文件夹整理" |
| **写代码** | "在这项目里加一个用户登录 API" |
| **处理 PDF** | 拖入 PDF → "帮我提取关键信息并总结" |
| **写文档** | "根据这个项目代码生成 README" |
| **网页研究** | "搜索最新的 .NET 9 新特性" |
| **数据处理** | 传 CSV → "分析这份数据并给出趋势图代码" |

### 7.3 从国内免费 API 接入（省订阅费用）

配合 Claude Desktop 的第三方兼容网关（如 OpenRouter），可以用国内更便宜的模型：

| 服务商 | 免费模型 | 说明 |
|--------|----------|------|
| **DeepSeek** | deepseek-chat / deepseek-reasoner | <https://platform.deepseek.com> |
| **智谱 GLM** | GLM-4-Flash（完全免费） | <https://open.bigmodel.cn> |
| **Moonshot** | moonshot-v1-8k | <https://platform.moonshot.cn> |

配置第三方网关（以 OpenRouter 为例）：
```
export ANTHROPIC_BASE_URL=https://openrouter.ai/api/v1
export ANTHROPIC_API_KEY=你的OpenRouter密钥
```

> OpenRouter 有大量免费模型：deepseek/deepseek-chat:free、google/gemini-2.0-flash:free 等

---

## 八、总结 — 免费实操路线图

```
安装流程（全部免费）：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣  下载 Claude Desktop → claude.ai/download
2️⃣  安装 Node.js → nodejs.org
3️⃣  安装 Git for Windows → git-scm.com
4️⃣  申请 Brave Search API Key → brave.com/search/api（免费2000次/月）
5️⃣  编辑 claude_desktop_config.json → 添加 MCP 服务器
6️⃣  重启 Claude Desktop → 看到 🔨 图标 = 成功！

推荐免费 MCP 优先级：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 必装：filesystem + fetch + memory + thinking + context7
🟡 推荐：brave-search（2000次/月免费）
🟢 按需：github + 其他社区 MCP
```

---

## 九、资源链接汇总

| 资源 | 链接 |
|------|------|
| Claude Desktop 下载 | <https://claude.com/download> |
| Claude Code 文档 | <https://code.claude.com/docs> |
| MCP 协议官网 | <https://modelcontextprotocol.io> |
| Awesome MCP Servers | <https://github.com/punkpeye/awesome-mcp-servers> |
| MCP Servers 精选列表 | <https://github.com/danielrosehill/Claude-Code-MCP-List> |
| Brave Search API | <https://brave.com/search/api/> |
| Node.js 下载 | <https://nodejs.org> |
| Skills 安装教程 | <https://www.agensi.io/learn/how-to-install-skills-claude-code> |
| Claude Desktop 扩展 | <https://www.anthropic.com/engineering/desktop-extensions> |
| MCP 中文文档 | <https://mcp.fleeto.us> |
