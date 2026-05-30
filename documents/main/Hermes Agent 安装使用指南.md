# Hermes Agent 安装使用指南（2026-05）

> Hermes Agent 是 Nous Research 于 2026-02-26 发布的开源自学习 AI Agent，GitHub 61K+ Stars。核心卖点：**运行时间越长越聪明**——自动从任务中创建技能、跨会话持久记忆、支持 6 种执行后端。

---

## 一、系统要求

| 项目 | 要求 |
|------|------|
| 操作系统 | Linux / macOS / WSL2（Windows）/ Termux（Android） |
| Python | 3.11+（安装脚本自动处理） |
| Git | 2.0+ |
| 内存 | 最低 4GB（推荐 8GB） |
| 网络 | 能访问模型 API 提供方 |

> ⚠️ Windows 原生支持仍处于早期测试版，**强烈推荐用 WSL2**。

---

## 二、安装（一行命令）

### Linux / macOS / WSL2（推荐）

```bash
# 一键安装（官方源）
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 国内镜像源（中国大陆用户优先，速度更快）
curl -fsSL https://res1.hermesagent.org.cn/install.sh | bash
```

安装完成后重启终端，验证：
```bash
source ~/.bashrc      # Bash
source ~/.zshrc       # Zsh
hermes --version      # 应显示 v0.8.0+
hermes doctor         # 检查环境配置
```

### Windows（PowerShell）

```powershell
# 官方源
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)

# 国内镜像源（推荐）
irm https://res1.hermesagent.org.cn/install.ps1 | iex
```

安装完成后**重启 PowerShell 窗口**（PATH 生效）。

### Android（Termux）

```bash
pkg update -y && pkg install -y git curl python
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install-termux.sh | bash
source ~/.bashrc
hermes doctor
```

### 手动安装（开发者/高级用户）

```bash
# 克隆仓库（含子模块）
git clone --recurse-submodules https://github.com/NousResearch/hermes-agent.git
cd hermes-agent

# 用 uv 创建虚拟环境
pip install uv
uv venv
source .venv/bin/activate
uv pip install -e .[all]

# 验证
hermes --version
```

---

## 三、配置（关键步骤）

### 1. 运行配置向导

```bash
hermes setup
```

向导会引导你完成：
- 选择 LLM 提供商
- 填入 API Key
- 配置默认工具集
- 设置基础偏好

建议新手选**快速设置**模式。

### 2. 选择大模型

Hermes 原生支持以下提供商（`hermes model` 命令切换，无需改代码）：

| 提供商 | 说明 | 适合场景 |
|--------|------|---------|
| **Kimi/Moonshot** | 国内用户首选，中文理解强，无需特殊网络 | 国内用户日常使用 |
| **OpenRouter** | 200+ 模型可选，有免费模型 | 预算有限 / 多模型切换 |
| **Nous Portal** | 官方原生集成，Hermes 系列模型 | 最佳 Hermes 体验 |
| **OpenAI** | GPT 系列 | 有 ChatGPT Pro 订阅 |
| **Anthropic** | Claude 系列 | Max 订阅用户 |
| **MiniMax** | M2.5 免费模型 | 免费使用 |
| **z.ai/GLM** | 智谱 GLM | 国内用户备选 |
| **NVIDIA NIM** | Nemotron 等 | 本地 GPU 推理 |
| **自定义 endpoint** | 任意兼容 OpenAI API 的端点 | 本地 Ollama 等 |

国内用户推荐配置：**Kimi + OpenRouter 免费模型** 组合，零成本起步。

### 3. 配置消息网关（可选）

用手机随时聊天：
```bash
hermes gateway setup
```
支持平台：Telegram、Discord、Slack、WhatsApp、Signal、Email

---

## 四、快速上手

### 基础命令

| 命令 | 用途 |
|------|------|
| `hermes` | 启动交互式 CLI 对话 |
| `hermes setup` | 运行全量配置向导 |
| `hermes model` | 选择/切换大模型 |
| `hermes tools` | 配置工具集 |
| `hermes gateway` | 启动消息网关（Telegram 等） |
| `hermes update` | 更新到最新版 |
| `hermes doctor` | 诊断运行环境 |
| `hermes claw migrate` | 从 OpenClaw 迁移数据 |

### 对话中常用斜杠命令

| 命令 | 功能 |
|------|------|
| `/model [provider:model]` | 实时切换模型 |
| `/tools` | 查看当前可用工具 |
| `/status` | 查看会话状态 |

### 第一个任务

安装配置完成后，直接在终端输入 `hermes` 开始对话，试试：

```
你：帮我分析一下 /home 目录下最大的 10 个文件
你：帮我总结一下今天的新闻
你：创建一个定时任务，每天早上 8 点提醒我喝水
```

Hermes 会自动调用工具执行，完成任务后会**自动将这次经验提炼为新技能**。

---

## 五、核心概念

### 🧠 Skill（技能）系统
- Hermes 完成任务后自动创建 Skill
- Skill 存储在 `~/.hermes/skills/`
- 下次遇到类似任务自动调用已有 Skill
- **越用越聪明**的核心机制

### 💾 持久化记忆
- 跨会话全文搜索记忆
- 存储在 `~/.hermes/memory/`
- 主动提示自身持久化知识
- 持续深化对用户认知的建模

### ⚙️ 执行后端（6 种）

| 后端 | 用途 | 成本 |
|------|------|------|
| `local` | 本地执行 | 免费 |
| `docker` | Docker 隔离环境 | 免费 |
| `ssh` | 远程服务器 | 免费（自备服务器） |
| `daytona` | Serverless 持久化 | $5/月 VPS 级别 |
| `singularity` | HPC 高性能集群 | 免费（自备集群） |
| `modal` | 云端函数执行 | 按量计费 |

切换后端：`hermes config set terminal.backend docker`

---

## 六、从 OpenClaw 迁移

如果你已经在用 OpenClaw，Hermes 可以一键导入：

```bash
# 查看迁移选项
hermes claw migrate --help

# 干运行预览（不实际执行）
hermes claw migrate --dry-run

# 执行迁移
hermes claw migrate
```

会导入：设置、记忆、技能和 API 密钥。

---

## 七、B 站学习视频推荐

### 入门必看

| 视频 | 内容简介 |
|------|---------|
| [Mac 装爱马仕 AI 保姆级教程｜一行命令 3 分钟跑起来](https://www.bilibili.com/video/BV1pRDxBuEsW) | Mac 安装 + 配置 + 连接 Telegram，适合新手 |
| [Windows 用户必看！Hermes Agent 安装全流程（无死角版）](https://www.bilibili.com/video/BV1wxd9BhEmK) | Windows WSL2 完整安装 + 飞书配置 |
| [Hermes Agent 从入门到精通（一）概念篇](https://www.bilibili.com/video/BV1s3DtBjEgt) | 核心概念、架构原理，华为团队出品 |

### 部署实战

| 视频 | 内容简介 |
|------|---------|
| [Hermes Agent 保姆级部署对接微信+飞书+Telegram](https://www.bilibili.com/video/BV128QvBgEzZ) | 最省钱方案 + 三大聊天通道对接 |
| [全 B 站最详细部署教程，从安装到跑通](https://www.bilibili.com/video/BV1M6oMB7E9w) | 完整避坑指南 + LLM-Wiki 知识库搭建 |
| [新手装完 Hermes 先学这 5 招](https://www.bilibili.com/video/BV1oMopBvEzs) | 每日进化面板 + WebUI + 可视化操作 |

### 进阶多 Agent

| 视频 | 内容简介 |
|------|---------|
| [Hermes Agent 从入门到精通（五）多代理 AI 团队](https://www.bilibili.com/video/BV1oMopBvEzs) | 从零构建多 Agent 协作团队 |
| [Hermes Agent 进阶：多智能体+知识库+Web UI](https://www.bilibili.com/video/BV1wxd9BhEmK) | 进阶玩法全解析 |

---

## 八、常见问题

**Q: 国内用户用什么模型最省钱？**
A: Kimi（Moonshot）+ OpenRouter 免费模型。Kimi 中文理解好，无需翻墙，注册送额度。

**Q: 和 OpenClaw 怎么选？**
A: OpenClaw 做通用助理（消息、日程、自动化），Hermes 做长期自学习任务。两者可以配合，Hermes 支持从 OpenClaw 迁移。

**Q: 安装报错怎么办？**
A: 先运行 `hermes doctor`，它会自动诊断并给出修复建议。

**Q: 免费吗？**
A: 软件本身免费（MIT 开源），服务器 $5-10/月，模型 API 可用免费模型（Kimi 有免费额度、OpenRouter 有免费 tier）。

---

## 九、官方资源

- 📖 官方文档（中文版）：https://hermes-agent.nousresearch.com/docs/zh-Hans
- 🐙 GitHub：https://github.com/NousResearch/hermes-agent
- 🌐 官网：https://hermes-agent.org

---

*数据来源：hermes-agent.nousresearch.com、GitHub README.zh-CN.md、CSDN（2026-05-25）、博客万（2026-05-13）、飞书官方教程、菜鸟教程。*
