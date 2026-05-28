# 📦 Skill 制作教程：OpenClaw & Claude Code

> 整理时间：2026年5月28日  
> 本视频推荐列表覆盖 B站上 OpenClaw Skills 与 Claude Code Skills 的入门教程、制作指南和实战案例，适合从零开始学习 Agent Skill 开发的同学。

---

## 📖 Skills 是什么？与 MCP、Slash Commands 的区别

### Skills（技能包）
Skills 是一种**给 AI Agent 安装的"知识包"或"工作流说明书"**。本质上是一个 `SKILL.md` 文件（或 YAML + Markdown 组合），描述了如何做某件事的步骤、工具和约束。Agent 在遇到匹配任务时自动加载对应的 Skill 来指导行为。

- **存储位置：** 本地文件夹（OpenClaw：`~/.agents/skills/`，Claude Code：`.claude/skills/`）
- **核心文件：** `SKILL.md`（YAML frontmatter + Markdown 指令）
- **作用：** 给 Agent 注入领域专业知识、标准化工作流程、减少重复提示词

### Skills vs MCP vs Slash Commands

| 维度 | Skills（技能包） | MCP（模型上下文协议） | Slash Commands |
|------|-----------------|----------------------|----------------|
| **本质** | Markdown 知识/指令文件 | 标准化工具调用协议 | 快捷命令触发器 |
| **作用** | 指导 Agent **如何做** | 让 Agent **调用外部工具** | 让用户**快速触发**特定行为 |
| **类比** | 操作手册/菜谱 | USB 接口标准 | 快捷键 |
| **示例** | "如何制作PPT"的步骤说明 | 连接数据库、文件系统的工具 | `/review` 触发代码审查 |
| **适用范围** | OpenClaw、Claude Code 等 | 支持 MCP 的所有 Agent 客户端 | Claude Code、Cursor 等 |
| **相互关系** | Skills 可以描述"何时使用哪个 MCP" | MCP 提供能力，Skills 提供使用方式 | Skills 可以被 Command 调用 |

> 💡 **一句话理解：** MCP 让 Agent 有手，Skills 让 Agent 有脑，Slash Commands 让用户有遥控器。

---

## 🦞 OpenClaw Skills 制作入门

以下视频专注于 OpenClaw 平台下的 Skills 安装、配置与自定义开发。

### 1. [手把手安装OpenClaw龙虾必备的技能Skills！](https://www.bilibili.com/video/BV1WAwxzPEud/)
> **简介：** 保姆级教程，从零安装 OpenClaw 并配置必备 Skills，适合第一次接触 OpenClaw 的新手。

### 2. [【保姆级】OpenClaw 全网最细教学：安装→Skills实战→多Agent协作](https://www.bilibili.com/video/BV1TpAZzeEiZ/)
> **简介：** 一小时全面精通 OpenClaw，涵盖安装、Skills 实战和多 Agent 协作的完整工作流。

### 3. [2026手把手教会你OpenClaw实战案例玩法，本地部署/接入微信/飞书/钉钉](https://www.bilibili.com/video/BV1bKwFzKE9L/)
> **简介：** 包含 Skills 和自定义 Skill 内容的综合实战案例，覆盖消息接入和自动化场景。

### 4. [OpenClaw从中级到高级完整教程](https://www.bilibili.com/video/BV1ZiNwzPEhP/)
> **简介：** 高级用法讲解，含 36 个实战案例演示，适合已有基础想深入学习的用户。

### 5. [【2026开发必备】Agent Skills零基础工业级实战！OpenClaw Skills系统...](https://www.bilibili.com/video/BV12VZXBqECz/)
> **简介：** 从零开发 Agent Skills，讲解技术实现流程和系统开发思路，适合开发者。

---

## 🤖 Claude Code Skills 制作入门

以下视频专注于 Claude Code 平台下的 Skills 开发和使用。

### 1. [【手把手教程】开发自己的Claude Agent Skills](https://www.bilibili.com/video/BV166sTzvEfd/)
> **简介：** 从 0 到 1 开发 Claude Agent Skills，包含 YAML frontmatter 编写和 Markdown 指令设计。

### 2. [一个视频让你彻底掌握Claude Code Skills](https://www.bilibili.com/video/BV1SqUCBoEDz/)
> **简介：** 从安装到使用全流程讲解，详解 Skills 与 MCP 的关系，适合系统性学习。

### 3. [Agent Skills (Claude Skills) 详细攻略，一期视频精通](https://www.bilibili.com/video/BV1HuiyBQE9G/)
> **简介：** 专注 Claude Skills 的深度攻略，分析 Skill 的适用场景和最佳实践。

### 4. [Claude Code 从0 到1 全攻略：MCP / SubAgent / Agent Skill / Hook / 图片识别](https://www.bilibili.com/video/BV14rzQB9EJj/)
> **简介：** 全覆盖教程，涵盖 Agent Skill 在内的 Claude Code 核心功能体系。

### 5. [【2026版Agent Skills保姆级教程】2小时从会用到会造](https://www.bilibili.com/video/BV1ahFmzqE9z/)
> **简介：** 2 小时深度课程，从使用 Skill 到自主开发，包含财务报表分析等实战案例。

---

## 🛠️ Skills 实战案例

以下视频展示了 Skills 在实际场景中的应用效果。

### 1. [Claude Code + PPT Skills 10分钟！保姆级教程！生成可编辑科研汇报PPT！](https://www.bilibili.com/video/BV1xYwgztESh/)
> **简介：** 用 Claude Code 的 PPT-Master Skill 10 分钟生成可编辑的科研汇报 PPT，效果惊艳。

### 2. [SKILL到底有什么用? 抓包拆解SKILL本质？](https://www.bilibili.com/video/BV1DQ6wBoEtN/)
> **简介：** 通过抓包分析 Skill 的实际运行机制，深入理解 Skill 的本质和工作原理。

### 3. [AI编程核心概念梳理：Rules/Commands/Subagent/Mcp/Skills/Modes/Hooks的区别](https://www.bilibili.com/video/BV1i7zKBkEdo/)
> **简介：** 系统梳理 AI 编程中的核心概念，一次搞清楚 Skills、MCP、Hooks 等概念的区别。

### 4. [Claude Skills 零基础入门自动化写作工作流及上线部署案例教学](https://www.bilibili.com/video/BV1nmkwB7Ed6/)
> **简介：** Claude Skills 实战营直播课，演示自动化写作工作流的搭建和部署。

### 5. [还在手动整理文档喂给Claude Code？Skill Seeker让AI变身全栈专家](https://www.bilibili.com/video/BV1R2sZzYE5T/)
> **简介：** 演示 Skill Seeker 这个 GitHub 知识库 Skill，让 AI 自动检索和整理文档。

---

## 📚 Skills 资源推荐

### 官方资源
- **OpenClaw 官方文档：** [docs.openclaw.ai](https://docs.openclaw.ai) — Skills 编写规范和 API 参考
- **Claude Code Skills 文档：** [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/skills) — Anthropic 官方 Skills 指南

### Skill 市场 / 仓库
- **ClawHub（OpenClaw 技能市场）：** [clawhub.com](https://clawhub.com) — OpenClaw 官方 Skills 市场，可一键安装社区 Skills
- **Claude Code Plugins 官方仓库：** [github.com/anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — Anthropic 官方维护的插件和 Skills
- **awesome-claude-code-skills：** GitHub 上搜索 `awesome-claude-code-skills` 可找到社区整理的 Skills 合集

### 社区文章
- **ClawHub Skills 技能全攻略（B站专栏）：** [cv46500097](https://www.bilibili.com/read/cv46500097) — 包含 ClawHub 介绍、CLI 安装、10 款高人气 Skills 详细说明
- **2天10万Star！GitHub史上最快开源项目OpenClaw（B站专栏）：** [cv45188007](https://www.bilibili.com/read/cv45188007) — OpenClaw 项目背景和技术架构介绍

### 推荐 GitHub 仓库
| 仓库 | 说明 |
|------|------|
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | Claude Code 官方仓库 |
| [openclaw-ai/openclaw](https://github.com/openclaw-ai/openclaw) | OpenClaw 官方仓库 |
| [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 官方 Claude 插件和 Skills |

---

## 💡 学习路径建议

```
新手入门
  │
  ├─ 1️⃣ 先理解概念：看「Skills vs MCP vs Slash Commands」相关视频
  │
  ├─ 2️⃣ 安装体验：跟着 OpenClaw / Claude Code 安装教程走一遍
  │
  ├─ 3️⃣ 使用现有 Skills：从 ClawHub 或官方市场安装几个热门 Skills 体验
  │
  ├─ 4️⃣ 学习制作：跟着「手把手开发自己的 Skills」教程写第一个 SKILL.md
  │
  └─ 5️⃣ 实战进阶：参考案例视频，为自己的工作流定制专属 Skills
```

> 📝 **提示：** 制作 Skill 的核心就是写好 `SKILL.md`——YAML 部分定义元数据（名称、描述、触发条件），Markdown 部分写清楚步骤和约束。从模仿开始，逐步迭代！
