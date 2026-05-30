# B站 Agent Skill 开发教程汇总

> 📅 采集日期：2026-05-30
> 🔍 搜索关键词：`Agent Skill 教程` `Claude Skills 开发` `OpenClaw Skill`
> 📊 共收录 **8个核心视频**，按分类整理

---

## 一、入门必看（零基础）

### 1. Claude Skill 保姆级教程！10分钟从0到1
- **UP主**：大模型Agent
- **链接**：<https://www.bilibili.com/video/BV1jD6MBQEfQ>
- **时长**：11分28秒
- **内容亮点**：
  - Agent Skill 的本质是什么
  - 演示安装和使用 Skills
  - 讲解 Skill 的 YAML frontmatter 结构
  - 如何从零写一个 Skill

### 2. 【手把手教程】开发自己的Claude Agent Skills
- **UP主**：图灵官方（01Coder）
- **链接**：<https://www.bilibili.com/video/BV166sTzvEfd>
- **时长**：17分10秒
- **播放量**：29.8万
- **内容亮点**：
  - 手把手完成第一个 Skill 开发
  - 从 SKILL.md 编写到实际测试全流程
  - 适合有编程基础的开发者入门

---

## 二、系统教程（从入门到实战）

### 3. 【2026版Agent Skills保姆级教程】2小时从会用到会造
- **UP主**：博学谷（传智教育旗下）
- **链接**：<https://www.bilibili.com/video/BV1ahFmzqE9z>
- **时长**：约2小时（15集）
- **内容亮点**：
  - 什么是 Agent Skills（系统讲解）
  - Skills 的安装与下载方法
  - 用 Skill 做企业网站设计 / 财务报表分析 / 一键生成视频 / LOGO设计 / 本地文件整理
  - **Skill 开发规则**（第10集）— 编写规范
  - **开发自动周报 Skill**（第11集）— 实战案例
  - **什么场景该上 Skill**（第13集）— 判断标准
  - **AgentSkills 核心机制剖析**（第14集）— 底层原理
  - Claude Code 等其他智能体使用 Skills（第15集）

### 4. 2026年吃透 - Agent Skills 从原理到实战全集
- **UP主**：图灵官方视频号
- **链接**：<https://www.bilibili.com/video/BV1F7cvzQE1K>
- **内容亮点**：
  - 从原理到代码实战开发
  - 企业级 Agent 智能体开发
  - 零基础小白友好

---

## 三、原理深度（底层机制）

### 5. Agent Skill 从使用到原理，一次讲清 ⭐推荐
- **UP主**：马克的技术工作坊（23.3万粉）
- **链接**：<https://www.bilibili.com/video/BV1cGigBQE6n>
- **时长**：约40分钟
- **播放量**：66.1万 | **点赞**：750
- **内容亮点**：
  - ⭐ Agent Skill 本质是什么
  - ⭐ 背后所使用的**渐进式披露机制**（Progressive Disclosure）
  - ⭐ Agent Skill 与 MCP 的区别，到底应该选哪个
  - 从 LLM 到 Skill 的底层逻辑打通

### 6. AgentSkill开发技术深度指南：从设计原则到工程实践
- **UP主**：图灵学院官方号
- **链接**：<https://www.bilibili.com/video/BV1ZsFbzZE5a>
- **时长**：约40分钟（3集）
- **内容亮点**：
  - 技能架构设计原则
  - 开发流程标准化
  - 质量控制和部署优化
  - 自定义 Skill 实战（代码审查 + SQL 助手）

### 7. 【通义实验室】AgentScope1.0 开发者教程：Agent Skills
- **UP主**：通义实验室（阿里官方）
- **链接**：<https://www.bilibili.com/video/BV1w4BYBtENL>
- **时长**：16分24秒
- **内容亮点**：
  - AgentScope 1.0 框架下的 Skills 开发
  - 阿里官方出品，工程化视角
  - 多智能体框架中的 Skills 实践

---

## 四、OpenClaw 专题

### 8. 建议收藏！2026唯一讲明白OpenClaw原理
- **UP主**：九天Hector
- **链接**：<https://www.bilibili.com/video/BV1hAcjzJEan>
- **时长**：约3小时（17集）
- **播放量**：10.7万
- **内容亮点**：
  - Agent Skill 系统设计思路
  - 无限上下文记忆机制
  - 自主迭代功能设计
  - Mini-OpenClaw 从零开发实战

---

## 五、UP 主推荐（持续产出 Skill 相关内容）

| UP主 | 粉丝 | 特色 | 空间链接 |
|------|------|------|----------|
| 马克的技术工作坊 | 23.3万 | 原理讲得最透，实战案例多 | <https://space.bilibili.com/1815948385> |
| 图灵官方 | 7.7万 | 系统教程完整 | <https://space.bilibili.com/3546575687241384> |
| 飞天闪客 | 23.6万 | 底层原理拆解 | <https://space.bilibili.com/325864133> |

---

## 六、核心知识点速查

### SKILL.md 结构
```yaml
---
name: your-skill-name
description: "触发描述，决定 Agent 何时使用该 Skill"
allowed-tools:
  - read
  - write
  - exec
---

# 标题

具体指令内容...
```

### Skill 设计最佳实践（来自视频总结）

1. **命名规范**：`kebab-case`，简短描述功能
2. **description 是关键**：写得越精准，触发越准确
3. **精简内容**：SKILL.md 是"即时索引"，不是完整文档
4. **渐进式披露**：先给核心指令，复杂细节按需加载
5. **场景判断**：重复性高 + 多步骤 → 适合做成 Skill

### Skill vs MCP 选择
| 对比项 | Skill | MCP |
|--------|-------|-----|
| 本质 | Markdown 指令文档 | 工具调用协议 |
| 作用域 | 行为规范 | 能力扩展 |
| 适用 | 流程、规范、模板 | 外部系统连接 |
| 优先级 | 先 Skill，再 MCP | 配合使用 |

---

> 📝 **注**：所有链接已验证可访问（2026-05-30）。视频内容以 UP 主实际发布为准。
