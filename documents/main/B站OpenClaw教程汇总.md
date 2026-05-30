# B站 OpenClaw 教程汇总

> 📅 采集日期：2026-05-30
> 🔍 搜索关键词：`OpenClaw 教程` `OpenClaw 配置` `OpenClaw skill 开发` `Clawdbot` `Moltbot`
> 📊 共收录 **12个核心视频**，按学习路径分类整理

---

## 一、学习路径总览

```
入门新手                进阶使用者              高阶开发者
─────────────────────────────────────────────────────
[安装部署系列]    →    [Skills 系列]     →    [原理与实战系列]
 _windows/mac          _Tavily/搜索          _MCP/SubAgentHook
  _Linux/Docker        _多Agent协作           _从零手搓OpenClaw
  _飞书/微信/钉钉       _定时任务/cron         _AI数字员工开发
  _国产模型接入         _浏览器控制            _企业级项目实战
```

---

## 二、入门安装（从0到跑起来）

### 1. 【保姆级】OpenClaw 全网最细教学：安装→Skills实战→多Agent协作 ⭐推荐
- **UP主**：AI学长小林（5.6万粉）
- **链接**：<https://www.bilibili.com/video/BV1TpAZzeEiZ>
- **时长**：53分25秒
- **播放量**：56.1万
- **视频笔记**：<https://ai.linbintalk.com/article/ytopenclaw>
- **内容亮点**：
  - 从零安装配置全流程
  - OpenClaw vs Claude Code 的核心差异（终端单兵 vs 24h AI团队）
  - 为什么 OpenClaw 能融入日常生活（接入 Telegram/飞书/WhatsApp）
  - 多智能体设置实践
  - Skills 添加与实战应用
  - 自动收集行业资讯、发小红书、发公众号等真实场景

### 2. OpenClaw 海量全玩法攻略（国内网络使用 + 本地部署）
- **UP主**：技术爬爬虾（38.2万粉）
- **链接**：<https://www.bilibili.com/video/BV1kH6nBFEPq>
- **播放量**：71.4万
- **内容亮点**：
  - Clawdbot/Moltbot/OpenClaw 名称演变历史
  - 几十个真实玩法案例大全
  - **国内网络适配方案**（接入飞书+国产模型）
  - 炒股/情报收集/收藏夹管理等实用场景

### 3. OpenClaw 开发全集（从入门到进阶）
- **UP主**：开发者LaoJ
- **链接**：<https://www.bilibili.com/video/BV1wAArzVE7q>
- **集数**：约15集完整系列
- **内容亮点**：
  - OpenClaw 安装部署全流程
  - 网关系统详解
  - Skills 系统详解
  - 插件与持久记忆系统
  - AI 数字员工功能介绍
  - 手把手打造一个自动化 Skill（第6集）

### 4. OpenClaw 详细安装配置和使用（三系统全覆盖）
- **UP主**：丨一丨丨二丨丨三丨
- **链接**：<https://www.bilibili.com/video/BV1LxXBBeE4E>
- **集数**：19集
- **内容亮点**：
  - Windows / macOS / Linux 三系统安装教程
  - Docker 下安装
  - 本地模型接入（Ollama）
  - 接入钉钉/飞书全流程
  - 阿里云/腾讯云一键部署

---

## 三、Skills 专项（核心能力）

### 5. OpenClaw 功能配置、定时任务安排和 Skills 下载安装
- **UP主**：技术爬爬虾
- **链接**：<https://www.bilibili.com/video/BV15wAhzPEMs>
- **内容亮点**：
  - OpenClaw Skills 系统全景介绍
  - cron 定时任务配置方法
  - Skills 下载、安装、管理实操

### 6. 3 分钟搞定！OpenClaw 接入 Tavily Search API
- **UP主**：杰森的效率工坊
- **链接**：<https://www.bilibili.com/video/BV19BZXBJEP8>
- **内容亮点**：
  - 注册 Tavily → 填入 API Key → 重启 OpenClaw
  - 极速接入网络搜索能力

### 7. 手把手配置 OpenClaw 使用任意平台模型
- **UP主**：博奥IT教育老段工作室
- **链接**：<https://www.bilibili.com/video/BV1ru62BPEBs>
- **内容亮点**：
  - 阿里百炼等国产大模型接入
  - 中转 API 配置方法

---

## 四、原理深度（开发者必看）

### 8. OpenClaw 原理精讲与从零手搓（7集完整系列）⭐推荐
- **UP主**：九天Hector（13.9万粉）
- **链接**：<https://www.bilibili.com/video/BV1mScqzqEDN>
- **时长**：约2小时（7集）
- **播放量**：10.7万
- **内容亮点**：
  - ⭐ Session / Memory / Tools / Skills 四大系统底层架构拆解
  - ⭐ 无限对话记忆功能实现原理
  - ⭐ 热装载技能（Hot-swap Skills）机制
  - ⭐ 自主迭代进化功能设计思路
  - 借助 Vibe Coding 从零开发垂域专属 OpenClaw
  - 配套完整项目代码

### 9. Agent Skill 从使用到原理，一次讲清
- **UP主**：马克的技术工作坊（23.3万粉）
- **链接**：<https://www.bilibili.com/video/BV1cGigBQE6n>
- **播放量**：66.1万 | **点赞**：750
- **内容亮点**：
  - Agent Skill 本质是什么
  - **渐进式披露机制**（Progressive Disclosure）详解
  - Skill vs MCP 的区别与选择策略
  - 从 LLM 到 Skill 的底层逻辑打通

### 10. OpenClaw + Claude Code 最省 Token 配置
- **UP主**：AI超元域
- **链接**：<https://www.bilibili.com/video/BV18NfmBhEtH>
- **内容亮点**：
  - Claude Code Hooks 回调机制
  - Agent Teams 全自动开发
  - Token 成本优化策略

---

## 五、实战应用（真实项目）

### 11. OpenClaw + 飞书 企业级 AI 数字员工
- **UP主**：码同学（15.3万粉）
- **链接**：<https://www.bilibili.com/video/BV1WnXkBWEc9>
- **播放量**：13.8万
- **内容亮点**：
  - 智能 HR 助理开发全流程
  - 飞书全自动简历搜集分析
  - 面试语音分析 + 面试邀约信息同步
  - 一人公司利器打造
  - 比付费效果强百倍的企业级实战

### 12. OpenClaw 36 个实战案例
- **UP主**：开源项目盘点
- **链接**：<https://www.bilibili.com/video/BV16MP4ziExA>
- **播放量**：10.1万
- **内容亮点**：36个开箱即用的 OpenClaw 实战案例演示

---

## 六、UP 主推荐（持续产出 OpenClaw 内容）

| UP主 | 粉丝 | 特色 | 空间链接 |
|------|------|------|----------|
| AI学长小林 | 5.6万 | 全网最细入门教程，学完能直接上手 | <https://space.bilibili.com/1316597695> |
| 九天Hector | 13.9万 | 原理深度拆解，从零手搓 OpenClaw | <https://space.bilibili.com/385842994> |
| 技术爬爬虾 | 38.2万 | 玩法多，国内适配方案全 | <https://space.bilibili.com/316183842> |
| 马克的技术工作坊 | 23.3万 | Skill/MCP/Agent 原理讲得最透 | <https://space.bilibili.com/1815948385> |
| 零度解说 | 24.8万 | 本地模型部署，免费方案 | <https://space.bilibili.com/625267185> |
| 飞天闪客 | 23.6万 | 底层逻辑一次性拆穿 | <https://space.bilibili.com/325864133> |

---

## 七、OpenClaw 核心概念速查

### 名称演变
```
Clawdbot → Moltbot(2026.1.27) → OpenClaw(2026.1.30) ← 三个名字，同一项目
```

### 核心架构（四系统）
| 系统 | 用途 | 关键文件 |
|------|------|----------|
| Session | 对话会话管理 | 自动维护 |
| Memory | 跨会话持久记忆 | `MEMORY.md`, `memory/*.md` |
| Tools | 工具调用内置能力 | 系统内置 + 插件 |
| Skills | 可复用技能包 | `~/.agents/skills/*/SKILL.md` |

### Skills 安装路径（OpenClaw）
```
~/.agents/skills/<skill-name>/SKILL.md    ← 主技能目录
~/.openclaw/workspace/skills/<skill>/     ← 工作区技能目录
```

### 常用命令速查
```bash
# 安装
curl -fsSL https://openclaw.ai/install.sh | bash

# 启动
openclaw gateway run --port 18789

# 重启（配置生效）
openclaw gateway restart

# 模型管理
openclaw models list
openclaw models test <provider/model>

# Web UI
http://127.0.0.1:18789/chat

# 配置文件位置
~/.openclaw/openclaw.json       ← 全局配置
~/.openclaw/agents/*/agent/     ← Agent 配置目录
```

### 国内模型接入方案
```
方案A：中转 API（推荐新手）
  BaseURL: https://api.whatai.cc/v1
  协议: OpenAI-compatible
  
方案B：阿里百炼直连
  BaseURL: 百炼平台获取
  协议: OpenAI-compatible
  
方案C：本地模型（Ollama）
  免费、断网可用
  推荐: Qwen3 / GLM-4.7 / GPT-OSS
```

### Skill vs MCP 选择指南
| 对比项 | Skill | MCP |
|--------|-------|-----|
| 本质 | Markdown 指令文档 | 工具调用协议 |
| 作用域 | Agent 行为规范、流程模板 | 外部系统/工具连接 |
| 文件 | `SKILL.md` | Server 配置 |
| 适用 | 重复性流程、规范文档 | 数据库、API、硬件 |
| 优先级 | **先装 Skills**，再按需加 MCP | 配合使用 |

---

> 📝 **注**：
> 1. 所有链接已验证可访问（2026-05-30）
> 2. OpenClaw 更新频繁，部分界面可能因版本迭代略有不同
> 3. 建议配合视频笔记食用：<https://ai.linbintalk.com/article/ytopenclaw>
