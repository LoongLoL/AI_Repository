# Claude Code 安装使用指南（2026-05）

> 数据来源：Anthropic 官方文档（code.claude.com）、NxCode、codewithmukesh.com、DEV Community、B站教程等，截止 2026-05-30。

---

## 一、什么是 Claude Code

**Claude Code** 是 Anthropic 官方的终端 AI 编码 Agent。不是聊天机器人，而是直接跑在你终端里的编码助手——它能读取你的代码文件、编写代码、运行命令、处理 Git 操作、感知整个项目上下文，通过自然语言驱动完成开发任务。

**和 Claude.ai 聊天的区别：**

| Claude.ai 聊天 | Claude Code |
|---------------|-------------|
| 浏览器里用 | 终端里用 |
| 不能读你本地的文件 | 直接读写你的代码文件 |
| 一次性对话 | 感知整个项目上下文 |
| 不能执行代码 | 能运行命令、执行测试 |
| 适合问答 | 适合完整开发流程 |

---

## 二、安装

### 前置条件

- Node.js 18+
- 终端（macOS Terminal、Windows Terminal、Linux 终端、VS Code 内置终端均可）
- Anthropic 账号（需订阅 Pro 或使用 API Key）

### macOS / Linux（一行命令）

```bash
# 官方安装脚本
curl -fsSL https://claude.ai/install.sh | bash

# 或 Homebrew
brew install --cask claude-code
```

### Windows（PowerShell）

```powershell
# 官方安装脚本
irm https://claude.ai/install.ps1 | iex

# 或 cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### VS Code / Cursor（IDE 扩展）

在扩展商店搜索 **"Claude Code"** 直接安装，无需 CLI。

### 验证安装

```bash
claude --version
```

---

## 三、登录与配置

### 登录账号

```bash
claude
```

首次启动会提示登录，两种方式：

**方式 A：OAuth 登录（推荐订阅用户）**
- 浏览器会自动打开 Anthropic 登录页面
- 用你的 Claude.ai 账号登录即可
- 需要 Pro（$20/月）或 Max（$100-200/月）订阅

**方式 B：API Key（适合按量付费）**
```bash
# 环境变量方式
export ANTHROPIC_API_KEY="sk-ant-xxxxx"

# 或在 claude 内部配置
/config
```

> ⚠️ **免费 Claude 账号不支持 Claude Code**，需要 Pro 订阅或 API Key。

### 模型选择

| 模型 | 特点 | 推荐场景 |
|------|------|---------|
| **Sonnet 4.6** | 快速、性价比高 | 日常编码（80% 任务） |
| **Opus 4.7** | 最强推理、复杂任务 | 架构设计、多文件重构、复杂调试（20% 任务） |

切换方式：
- 对话中输入 `/model opus` 或 `/model sonnet`
- 或 `/model` 打开选择界面

---

## 四、快速上手（8 步走）

官方 Quickstart 流程，建议按顺序走一遍：

### Step 1：启动项目会话

```bash
cd /your/project
claude
```

### Step 2：问第一个问题

```
你能帮我总结一下这个项目的结构吗？
```

Claude 会主动读你的项目目录文件。

### Step 3：让 Claude 写代码

```
给 auth 模块写测试，跑一下，如果有失败的就修复
```

Claude 会读取文件 → 写代码 → 执行测试 → 修复错误。

### Step 4：操作 Git

```
帮我 review 一下最近的改动
git status / git diff
```

Claude 可以直接执行 git 命令。

### Step 5：修复 Bug

```
LoginPage 组件有个 bug：用户输入密码后点登录按钮没反应。
帮我定位并修复。
```

### Step 6：CLAUDE.md 项目记忆

在项目根目录创建 `CLAUDE.md`，Claude 每次启动会自动读取：

```markdown
# 项目：我的 Web 应用

## 技术栈
- 前端：React + TypeScript + TailwindCSS
- 后端：Node.js + Express
- 数据库：PostgreSQL

## 代码规范
- 用 2 空格缩进
- 组件用 PascalCase
- 文件名用 kebab-case

## 重要说明
- 不要用 any 类型
- 优先使用函数组件
```

### Step 7：Plan Mode（复杂任务必备）

遇到复杂任务，先用 Plan Mode 让 Claude 思考再执行：

```
/plan
然后在 plan 界面描述你的任务
```

Plan Mode 会：分析问题 → 列出步骤 → 等待你确认 → 执行。

### Step 8：常用斜杠命令速查

| 命令 | 功能 |
|------|------|
| `/model` | 切换模型 |
| `/plan` | 开启 Plan Mode |
| `/clear` | 清除上下文 |
| `/cost` | 查看本次会话 token 消耗 |
| `/config` | 打开配置面板 |
| `/review` | 请 Claude 审查当前变更 |
| `/help` | 帮助 |

---

## 五、核心功能

### 1. 多文件理解

Claude Code 能感知整个项目上下文，不是只看单个文件。你可以问：

```
这个 API 的参数从哪里传到哪里的？帮我画出调用链。
```

### 2. 权限系统

每次 Claude 要执行命令或修改文件，都会**先请求你确认**：

```
[Tool: Edit] 修改 /src/auth/login.tsx
  Allow this edit? (y/n)
```

防止 AI 乱改代码。

### 3. Plan Mode

复杂任务先规划再执行：
```
/plan
重构整个用户认证模块，从 JWT 迁移到 session-based
```

Claude 会输出一份详细计划，你确认后才开始执行。

### 4. Agent Teams（多 Agent 并行）

多个独立的 Claude 实例并行处理子任务：

```
用 3 个 subagent 并行处理：
- Agent 1: 写前端组件
- Agent 2: 写 API 接口
- Agent 3: 写测试
```

### 5. MCP 集成

通过 MCP（Model Context Protocol）扩展 Claude 的能力：

```bash
# 添加 MCP 服务器（Playwright 浏览器自动化）
claude mcp add playwright npx -y @playwright/mcp@latest

# 添加自定义工具
claude mcp add my-tool python my_mcp_server.py
```

常用 MCP 集成：
- Playwright（浏览器自动化）
- GitHub（PR 管理）
- 数据库（PostgreSQL、MongoDB）
- 文件系统

### 6. Skills

自定义可复用的工作流程：

```markdown
# ~/.claude/skills/my-skill/SKILL.md
---
name: my-skill
description: 我的自定义工作流
---

执行以下步骤：
1. 执行 X
2. 执行 Y
3. 输出 Z
```

---

## 六、费用

### 订阅方案

| 方案 | 价格 | 包含内容 |
|------|------|---------|
| **Free** | $0 | ❌ 不含 Claude Code |
| **Pro** | **$20/月** | Sonnet 4.6，有限 token 额度 |
| **Max 5x** | **$100/月** | 更高额度，Sonnet + Opus |
| **Max 20x** | **$200/月** | 最高额度，重度用户 |
| **Team** | $25-150/seat/月 | 团队管理，token 另算 |
| **Enterprise** | 定制 | 企业级功能 |

### API 按量付费

| 模型 | Input | Output |
|------|-------|--------|
| Sonnet 4.6 | $3/M tokens | $15/M tokens |
| Opus 4.7 | $5/M tokens | $25/M tokens |

### 隐藏计费点 ⚠️

1. **Pro/Max 与 Claude.ai 聊天共享 quota** — 聊天用完了 Claude Code 也停
2. **Team 版 token 另算** — 订阅费不含 token 用量
3. **上下文越大越贵** — 1M 上下文窗口意味着每轮可能消耗数万 token
4. **Agent Teams 并行 = 多倍 token** — 3 个 subagent 并行 ≈ 3 倍消耗
5. **Plan Mode 额外消耗** — 规划阶段也消耗 token

### 省钱建议

- 日常用 **Sonnet 4.6**，复杂任务才切 Opus
- 用 `/cost` 随时监控消耗
- 定期 `/clear` 清理上下文
- 大任务拆成多个会话，避免单会话上下文过大

---

## 七、B 站学习视频推荐

### 入门必看

| 视频 | 内容简介 |
|------|---------|
| [Claude Code 从零安装到上手｜注册+付费+避坑全流程](https://www.bilibili.com/video/BV1j5RWBYESR) | 安装、注册、付费、登录、封号避坑，国内用户必看 |
| [9分钟搞定！Claude Code 保姆级安装+原理+真实用法（国内直连）](https://www.bilibili.com/video/BV1NvRyBzEhq) | 快速上手，国内网络环境配置 |
| [Claude Code 全栈教程（字节大佬）](https://www.bilibili.com/video/BV1wuQEBDEN8) | 从入门到精通，Git/Node/阿里百炼三种模式 |

### 进阶实战

| 视频 | 内容简介 |
|------|---------|
| [Claude Code 从 0 到 1 全攻略：MCP/SubAgent/Skill/Hook](https://www.bilibili.com/video/BV1jiPjzqEjA) | 四大核心功能深度解析 |
| [B站最全：MCP 协议、Agent Skill 定制、Hook 钩子与后台任务](https://www.bilibili.com/video/BV1jiPjzqEjA) | 进阶功能全覆盖 |
| [Claude Code 企业级实战案例（2026 最新版）](https://www.bilibili.com/video/BV1zZwTzCEj8) | 大型项目改造、Playwright MCP 增强 Bug 修复 |

### 桌面版 & 国产模型

| 视频 | 内容简介 |
|------|---------|
| [ClaudeCode 桌面版 + DeepSeek！免登录免梯子](https://www.bilibili.com/video/BV1fXQxBYET3) | 桌面版使用 + 接入国产模型 |
| [Claude Code 保姆级速成（附完整文档）](https://www.bilibili.com/video/BV1NvRyBzEhq) | 快速上手，配套资料 |

---

## 八、常用工作流

### 日常开发流程

```bash
cd my-project
claude

# 1. 让 Claude 了解项目
"总结一下这个项目的架构"

# 2. 开发新功能
"实现用户注册功能，包括前端表单、API 接口、数据库 migration"

# 3. 写测试并运行
"给刚才的注册功能写测试，跑一下"

# 4. Code Review
/review

# 5. 提交代码
"帮我 commit 并 push，commit message 用 conventional commits"
```

### 大型项目重构

```bash
/plan
"把整个认证模块从 JWT 迁移到 session-based 认证"
# 确认计划后执行
```

### 调试 Bug

```bash
"LoginPage 组件的登录按钮点击没反应，帮我定位问题"
# Claude 会读代码、运行测试、逐步排查
```

---

## 九、常见问题

**Q: 免费账号能用吗？**
A: 不能。需要 Pro（$20/月）订阅或 API Key。

**Q: 国内怎么用？**
A: 需要海外网络环境。B站有教程介绍国内直连方案（通常通过代理或第三方 API 转发）。

**Q: 和 Cursor 怎么选？**
A: Cursor 是 IDE，适合喜欢 GUI 的用户；Claude Code 是终端 Agent，适合终端重度用户。两者可以配合用。

**Q: token 消耗太快怎么办？**
A: 用 Sonnet 替代 Opus；定期 `/clear`；大任务拆成多个会话；用 CLAUDE.md 减少重复说明。

**Q: 安全吗？Claude 会不会乱改代码？**
A: 每次修改都会请求你确认。你也可以在设置中调整权限模式。

---

## 十、官方资源

- 📖 官方文档：https://code.claude.com/docs/en/overview
- 🚀 Quickstart：https://code.claude.com/docs/en/quickstart
- 💬 社区：https://discord.com/invite/claude
- 🐦 更新公告：https://x.com/AnthropicAI

---

*数据来源：Anthropic 官方文档（code.claude.com）、NxCode（nxcode.io）、codewithmukesh.com、DEV Community、B站教程视频等，2026年5月。*
