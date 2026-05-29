# 如何让 OpenClaw 更多更好地使用 Skill

> 来源：OpenClaw 官方文档 + GitHub Issues + 社区最佳实践综合整理
> 原文链接：https://docs.openclaw.ai/tools/skills

---

## 一、为什么 Skill 没有被触发？

根据当前 session transcript 统计（273 次工具调用），发现：

| 问题 | 数据 | 原因 |
|------|------|------|
| exec 占 56% | 153 次 | agent 偏好用 shell 命令直接操作，而不是读 SKILL.md |
| web_search 占 21% | 57 次 | 搜索引擎直接可用，不需要经过 skill |
| 实际 read SKILL.md | 极少 | agent 很少主动读取 skill 文件 |

**根本原因：SKILL.md 加载机制是"懒加载"的。** OpenClaw 不会在启动时加载所有 skill，而是在 agent 判断需要某个能力时才去读对应的 SKILL.md。如果 agent 觉得用内置工具（exec/web_search）就能完成，就不会去读 skill。

---

## 二、让 Skill 更容易被触发的 6 个方法

### 方法 1：在 AGENTS.md 中明确引用 Skill

当前 AGENTS.md 没有提到任何具体 skill。在开头加入一段：

```markdown
## 可用 Skills（按场景采�用）

**新闻采集（优先级顺序）：**
1. news-summary — 从 BBC/Reuters/NPR/Al Jazeera 拉取 RSS 新闻摘要（先读 SKILL.md）
2. daily-ai-news — AI 领域新闻汇总
3. hackernews — Hacker News 热榜/评论

**文档处理：**
- pdf — 任何 PDF 操作（8个脚本）
- pptx — 任何 PPTX 操作（16个脚本）

**搜索增强：**
- firecrawl_search / firecrawl_scrape — 深度网页搜索/抓取
- tavily-search — AI 优化搜索

**复杂任务：**
- planning-with-files — 多步骤任务规划（创建 task_plan.md/findings.md/progress.md）
- chinese-novelist — 中文小说创作
```

**效果：** agent 每次启动都会看到这些提示，大幅提高触发概率。

---

### 方法 2：在 Skill 的 description 字段中写更具体的触发词

OpenClaw 通过 SKILL.md frontmatter 中的 `description` 来决定是否加载该 skill。**description 越具体、覆盖的关键词越多，被触发的概率越高。**

**改进前（当前 news-summary）：**
```yaml
description: news summary skill
```

**改进后（建议）：**
```yaml
description: |
  Fetch and summarize daily news from BBC, Reuters, NPR, Al Jazeera RSS feeds.
  Use when user asks for: news, today's news, daily briefing, world news,
  what's happening, current events, news summary, 新闻, 每日简报.
  Supports text summaries and OpenAI TTS voice output.
  Triggers on keywords: news, briefing, headlines, bbc, reuters.
```

**原则：**
- description 中列出所有可能的用户说法（中英文都写）
- 包含动词和名词变体（"搜索" "搜一下" "查一下" "news" "briefing"）
- 明确写出触发场景（"当用户问X时使用"）

---

### 方法 3：将 Skill 安装到更高优先级的路径

OpenClaw skill 加载优先级（从高到低）：

| 优先级 | 路径 | 范围 |
|--------|------|------|
| 1（最高） | `<workspace>/skills/` | Per-agent |
| 2 | `<workspace>/.agents/skills/` | Per-workspace agent |
| 3 | `~/.agents/skills/` | Shared agent profile |
| 4 | `~/.openclaw/skills/` | All agents |
| 5（最低） | Bundled skills | 随安装包 |

**当前 news-summary 安装在 `~/.openclaw/workspace/skills/`（优先级 1）**，已经是最高优先级。

但如果有自定义版本想覆盖，可以放到 `<workspace>/skills/` 目录下。

---

### 方法 4：在 Cron/Heartbeat 任务中直接指定 Skill

不要等 agent 自己判断，在定时任务中**明确指定使用哪个 skill**：

```json
{
  "name": "每日新闻采集",
  "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "使用 news-summary skill 获取今天的国际新闻简报。先读取 ~/.agents/skills/news-summary/SKILL.md，然后按照其中的工作流执行：从 BBC World News RSS 获取头条，从 Al Jazeera 获取全球视角，总结成中文简报推送给用户。"
  }
}
```

**关键点：** prompt 中明确写"先读取 SKILL.md" + "按照工作流执行"，而不是模糊地说"获取新闻"。

---

### 方法 5：精简 Skill 数量，提高命中率

当前有 **153 个 skill**，其中 78 个是 .NET 开发相关的。每次对话，agent 要从这么多 skill 中判断用哪个，反而会"选择困难"。

**建议：**
1. **归档不常用的 skill** — 把当前不需要的移到 `~/.agents/skills/archive/` 目录
2. **按场景创建 meta-skill** — 创建一个 `news-collector` skill，内部编排 news-summary + daily-ai-news + hackernews 三个 skill 的调用顺序
3. **每个 skill 的 description 互斥** — 避免多个 skill 描述相似场景，让 agent 知道"这个场景用这个，那个场景用那个"

---

### 方法 6：在 Skill 中嵌入明确的触发指令

在 SKILL.md 的 body 中加入 **Decision Tree（决策树）**，让 agent 能快速判断是否该用这个 skill：

```markdown
## Decision Tree

Use this skill when:
- User says "news" or "today's news" or "what's happening"
- User asks for a "daily briefing" or "morning summary"
- User mentions specific news sources (BBC, Reuters, NPR)
- Current time is morning (6-10 AM) and user says "good morning"

DO NOT use this skill when:
- User asks about a specific company/stock → use market-data instead
- User asks for HN trending → use hackernews instead
- User asks for AI-specific news → use daily-ai-news instead
```

---

## 三、当前新闻采集 Skill 配置建议

基于你的 4 个新闻 skill，推荐如下调用链：

```

用户请求"今天的新闻"
    ↓
agent 判断场景
    ↓
[国际时事] → news-summary（RSS，不依赖搜索，最稳定）
[AI 领域]  → daily-ai-news（定时聚合）
[科技社区] → hackernews（HN API）
[深度搜索] → firecrawl_search + tavily-search（后备）
```

**优先级：news-summary > daily-ai-news > hackernews > web_search**

---

## 四、快速验证

测试方法：直接问 agent 以下问题，观察它是否先 read SKILL.md 再执行：

```
"用 news-summary skill 获取今天的 BBC 世界新闻"
```

如果 agent 没有先 `read SKILL.md` 就执行，说明 description 不够清晰，需要按方法 2 修改。
