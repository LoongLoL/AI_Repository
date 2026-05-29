# OpenClaw Firecrawl 配合使用与搜索引擎配置完全指南

> 本文整合 OpenClaw 官方文档、阿里云开发者社区、w3cschool、Medium 等多方面资料，系统讲解 Firecrawl 与 OpenClaw 的配合使用方式，以及 OpenClaw 搜索引擎的完整配置方法。

---

## 一、Firecrawl 与 OpenClaw 配合使用

### 1.1 三种使用方式

OpenClaw 可以通过三种方式使用 Firecrawl：

| 使用方式 | 说明 | 适用场景 |
|---------|------|---------|
| **web_search 提供商** | 将 Firecrawl 设为默认搜索引擎 | 常规关键词搜索 |
| **显式插件工具** (`firecrawl_search` / `firecrawl_scrape`) | 作为独立工具调用 | 需要深度提取、结构化抓取 |
| **web_fetch 后备提取器** | 当普通 HTTP 抓取失败时自动降级到 Firecrawl | 处理 JS 密集型网站或反机器人防护页面 |

> 📄 原文链接：https://docs.openclaw.ai/zh-CN/tools/firecrawl

### 1.2 获取 API Key

1. 访问 [Firecrawl 官网](https://firecrawl.dev) 创建账户
2. 在 Dashboard 中生成 API Key（格式为 `fc-...`）
3. 存储方式二选一：
   - 在配置文件中设置 `FIRECRAWL_API_KEY`
   - 在 Gateway 环境变量中设置 `FIRECRAWL_API_KEY`

### 1.3 配置 Firecrawl 作为搜索引擎

**配置文件方式（json5）：**

```json5
{
  tools: {
    web: {
      search: {
        provider: "firecrawl",
      },
    },
  },
  plugins: {
    entries: {
      firecrawl: {
        enabled: true,
        config: {
          webSearch: {
            apiKey: "FIRECRAWL_API_KEY_HERE",
            baseUrl: "https://api.firecrawl.dev",
          },
        },
      },
    },
  },
}
```

**交互式配置方式（推荐新手）：**

```bash
openclaw configure --section web
```

选择 Firecrawl 即可自动启用内置插件。

**环境变量方式：**

```bash
export FIRECRAWL_API_KEY="fc-your-key-here"
export FIRECRAWL_BASE_URL="https://api.firecrawl.dev"  # 可替换为自托管地址
```

### 1.4 配置 Firecrawl 作为 web_fetch 后备

```json5
{
  plugins: {
    entries: {
      firecrawl: {
        enabled: true,
        config: {
          webFetch: {
            apiKey: "FIRECRAWL_API_KEY_HERE",
            baseUrl: "https://api.firecrawl.dev",
            onlyMainContent: true,    // 只提取正文内容
            maxAgeMs: 172800000,      // 缓存有效期 2 天
            timeoutSeconds: 60,       // 超时时间
          },
        },
      },
    },
  },
}
```

**配置说明：**
- `onlyMainContent: true` — 只返回页面正文，过滤导航/广告等噪音
- `maxAgeMs` — 缓存有效期（毫秒），默认 2 天
- `timeoutSeconds` — 抓取超时时间

### 1.5 使用 firecrawl_search 工具

当需要 Firecrawl 专用搜索控制时，使用此工具：

```javascript
await firecrawl_search({
  query: "AI news today",
  count: 10,
  sources: ["web", "news"],     // 指定搜索源
  categories: ["technology"],   // 分类筛选
  scrapeResults: true,          // 同时抓取结果页面内容
  timeoutSeconds: 30,
});
```

### 1.6 使用 firecrawl_scrape 工具

对于 JS 较重或受机器人防护的页面：

```javascript
await firecrawl_scrape({
  url: "https://example.com",
  extractMode: "markdown",  // 或 "text"
  maxChars: 8000,
  onlyMainContent: true,
  proxy: "auto",            // "auto" | "basic" | "stealth"
  storeInCache: true,
  timeoutSeconds: 60,
});
```

**Proxy 模式说明：**

| 模式 | 说明 |
|------|------|
| `basic` | 标准 HTTP 代理，规避基础反爬 |
| `stealth` | 高级隐身模式，应对严格的反机器人检测 |
| `auto` | 自动选择（推荐） |

### 1.7 自托管 Firecrawl

如果有私有部署需求：

```bash
# 设置自托管地址
export FIRECRAWL_BASE_URL="http://localhost:3002"
```

或通过配置文件：

```json5
{
  plugins: {
    entries: {
      firecrawl: {
        config: {
          webSearch: { baseUrl: "http://localhost:3002" },
          webFetch: { baseUrl: "http://localhost:3002" },
        },
      },
    },
  },
}
```

> ⚠️ 安全限制：OpenClaw 仅对 loopback、私有网络、`.local`、`.internal`、`.localhost` 目标接受 `http://` 协议。公共自定义主机会被拒绝，以防止 API key 意外泄露。

### 1.8 当前环境状态（本机）

| 项目 | 状态 |
|------|------|
| Firecrawl CLI | ✅ 已安装 (v1.18.5) |
| Firecrawl API Key | ❌ 未配置 |
| 代理 (`192.168.31.186:7890`) | ✅ 可用 |
| `web_fetch` 工具 | ⚠️ FireCrawl SDK 不走系统代理，DNS 解析失败 |
| 临时修复 | `NODE_OPTIONS=--use-env-proxy` 可使 Node.js fetch 走代理 |

> 📄 原文链接：
> - https://docs.openclaw.ai/zh-CN/tools/firecrawl
> - https://docs.openclaw.ai/zh-TW/tools/firecrawl
> - https://news-openclaw.smzdm.com/docs/zh-CN/tools/firecrawl
> - https://www.w3cschool.cn/openclawdocs/openclaw-tools-firecrawl.html
> - https://medium.com/@info.booststash/how-to-use-firecrawl-with-openclaw-for-advanced-web-scraping-00de1c637216

---

## 二、OpenClaw 搜索引擎配置

### 2.1 支持的搜索引擎一览

OpenClaw 支持 12 种搜索引擎提供商：

| 提供商 | 结果样式 | 筛选器 | API Key | 费用 |
|--------|---------|--------|---------|------|
| **Brave Search** | 结构化摘要片段 | 国家/地区、语言、时间、llm-context | `BRAVE_API_KEY` | 免费额度 |
| **DuckDuckGo** | 结构化摘要片段 | — | 无 | 免费 |
| **Exa** | 结构化 + 已提取 | 神经/关键词模式、日期、内容提取 | `EXA_API_KEY` | 免费 |
| **Firecrawl** | 结构化摘要片段 | 通过 `firecrawl_search` 工具 | `FIRECRAWL_API_KEY` | 按量付费 |
| **Gemini** | AI 综合 + 引用 | — | `GEMINI_API_KEY` | 付费 |
| **Grok** | AI 综合 + 引用 | — | `XAI_API_KEY` | 付费 |
| **Kimi** | AI 综合 + 引用 | — | `KIMI_API_KEY` | 付费 |
| **MiniMax Search** | 结构化摘要片段 | 区域（global/cn） | `MINIMAX_*` | 付费 |
| **Ollama Web 搜索** | 结构化摘要片段 | — | 无需/OLLAMA_API_KEY | 免费/付费 |
| **Perplexity** | 结构化摘要片段 | 国家/地区、语言、时间、域名、内容限制 | `PERPLEXITY_API_KEY` | 付费 |
| **SearXNG** | 结构化摘要片段 | 类别、语言 | 无（自托管） | 免费 |
| **Tavily** | 结构化摘要片段 | 通过 `tavily_search` 工具 | `TAVILY_API_KEY` | 免费额度 |

> 📄 原文链接：https://docs.openclaw.ai/zh-CN/tools/web

### 2.2 搜索引擎选择建议

**个人用户推荐方案（免费优先）：**

```
DuckDuckGo（零配置，无需 Key）
    ↓ 能力不够用时
SearXNG（自托管，免费，聚合多引擎）
    ↓ 需要更强的搜索能力
Exa.ai（免费无额度限制，可本地部署）
    ↓ 需要 AI 摘要
Brave Search（每月免费额度，隐私保护好）
```

**企业/专业用户推荐方案：**

```
Perplexity（深度搜索 + 多模型切换 + 文件解析）
    ↓ 需要 Google 生态集成
Gemini Search（额度充足，多模态搜索）
    ↓ 需要 X/Twitter 内容
Grok（xAI Web grounding）
    ↓ 需要国内搜索
Kimi / MiniMax（国内线路）
```

### 2.3 各搜索引擎详细配置

#### 2.3.1 SearXNG（推荐自托管）

**优势：** 免费、自托管、聚合 Google/Bing/DuckDuckGo 等多个搜索引擎。你家已部署 (`http://localhost:8080`)。

```json5
{
  tools: {
    web: {
      search: {
        provider: "searxng",
      },
    },
  },
  plugins: {
    entries: {
      searxng: {
        enabled: true,
        config: {
          baseUrl: "http://localhost:8080",
          engines: ["google", "bing", "duckduckgo"],
        },
      },
    },
  },
}
```

#### 2.3.2 DuckDuckGo（零配置首选）

**优势：** 无需 API Key，零配置，隐私保护。

```bash
# 直接配置即可使用
openclaw configure --section web
# 选择 DuckDuckGo
```

> ⚠️ 注意：基于非官方 HTML 集成，稳定性可能不如付费 API。

#### 2.3.3 Brave Search

**优势：** 每月免费额度（约 1000 次查询），隐私保护强。

1. 访问 [Brave Search API](https://search.brave.com/api) 注册
2. 获取 API Key（格式 `bs_...`）
3. 配置：

```json5
{
  tools: {
    web: {
      search: {
        provider: "brave",
      },
    },
  },
  plugins: {
    entries: {
      brave: {
        enabled: true,
        config: {
          apiKey: "BRAVE_API_KEY_HERE",
        },
      },
    },
  },
}
```

或通过环境变量：

```bash
export BRAVE_API_KEY="bs-your-key-here"
```

#### 2.3.4 Tavily

**优势：** 专为 AI Agent 优化，支持搜索深度控制和主题筛选。

```bash
export TAVILY_API_KEY="tvly-your-key-here"
```

```json5
{
  tools: {
    web: {
      search: {
        provider: "tavily",
      },
    },
  },
  plugins: {
    entries: {
      tavily: {
        enabled: true,
        config: {
          apiKey: "TAVILY_API_KEY",
        },
      },
    },
  },
}
```

#### 2.3.5 Perplexity

**优势：** 深度搜索能力强，多模型切换，支持文件解析。

```bash
export PERPLEXITY_API_KEY="pplx-your-key-here"
```

#### 2.3.6 Exa.ai

**优势：** 免费无额度限制，神经搜索 + 关键词搜索混合模式。

```bash
export EXA_API_KEY="your-key-here"
```

### 2.4 通过交互式命令配置（最简单）

```bash
# 运行交互式配置向导
openclaw configure --section web
```

按照提示选择搜索引擎并输入 API Key 即可。

### 2.5 环境变量速查表

```bash
# SearXNG
SEARXNG_BASE_URL=http://localhost:8080

# Brave
BRAVE_API_KEY=bs-xxx

# Tavily
TAVILY_API_KEY=tvly-xxx

# Perplexity
PERPLEXITY_API_KEY=pplx-xxx

# Firecrawl
FIRECRAWL_API_KEY=fc-xxx
FIRECRAWL_BASE_URL=https://api.firecrawl.dev

# Exa
EXA_API_KEY=xxx

# Gemini
GEMINI_API_KEY=xxx

# Kimi / Moonshot
KIMI_API_KEY=xxx
MOONSHOT_API_KEY=xxx

# MiniMax
MINIMAX_CODE_PLAN_KEY=xxx
```

> 📄 原文链接：https://docs.openclaw.ai/zh-CN/tools/web

---

## 三、OpenClaw 联网工具对比

| 工具 | 类型 | 能力 | 需要配置 | 适用场景 |
|------|------|------|---------|---------|
| `web_search` | 搜索 API | 关键词搜索 | 需要搜索引擎提供商 | 新闻查询、实时信息 |
| `web_fetch` | HTTP GET | 获取指定 URL 内容 | 可选 Firecrawl 后备 | 读取特定网页 |
| `browser` | 浏览器自动化 | JS 执行、登录、交互 | 需要浏览器 | 复杂交互页面 |

**三者配合使用场景示例：**

```
新闻采集工作流：
  web_search("今日新闻") → 获取新闻链接列表
  web_fetch(链接) → 读取新闻正文
  （如果 web_fetch 失败）→ Firecrawl 后备提取
  （如果需要登录/JS）→ browser 浏览器自动化
```

---

## 四、常见问题

### Q1: web_search 和 web_fetch 有什么区别？

- `web_search` 是**搜索引擎**，输入关键词返回搜索结果列表。
- `web_fetch` 是**网页抓取器**，输入 URL 返回页面内容。
- 两者互补：先用 `web_search` 搜到链接，再用 `web_fetch` 读取内容。

### Q2: 为什么 web_fetch 报 DNS 解析错误？

如果配置了 Firecrawl 作为后备提取器，FireCrawl SDK 可能没有走系统代理。解决方案：

```bash
# 在 Gateway 环境中设置
export NODE_OPTIONS="--use-env-proxy"
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
```

然后重启 Gateway。

### Q3: 可以不配置搜索引擎吗？

可以。不配置搜索引擎时：
- `web_search` 不可用
- 只能用 `web_fetch` 读取已知 URL
- AI 知识停留在训练数据截止日，无法获取实时信息

强烈建议至少配置 DuckDuckGo（免费，零配置）。

### Q4: SearXNG 和 DuckDuckGo 哪个好？

| 对比项 | SearXNG | DuckDuckGo |
|--------|---------|-----------|
| 费用 | 免费（需自托管） | 免费 |
| 配置 | 需要部署 | 零配置 |
| 能力 | 聚合多引擎，更强 | 基础搜索 |
| 隐私 | 自托管，完全可控 | 依赖第三方 |
| 稳定性 | 依赖自建服务 | 依赖官方服务 |

> 📄 原文链接汇总：
> - OpenClaw 官方文档（Firecrawl）：https://docs.openclaw.ai/zh-CN/tools/firecrawl
> - OpenClaw 官方文档（Web 搜索）：https://docs.openclaw.ai/zh-CN/tools/web
> - OpenClaw 官方文档（API 成本）：https://docs.openclaw.ai/reference/api-usage-costs
> - OpenClaw Firecrawl 技能教程（w3cschool）：https://www.w3cschool.cn/openclawdocs/openclaw-tools-firecrawl.html
> - Firecrawl + OpenClaw 爬虫实战（Medium）：https://medium.com/@info.booststash/how-to-use-firecrawl-with-openclaw-for-advanced-web-scraping-00de1c637216
> - OpenClaw 搜索引擎配置全指南（阿里云）：https://developer.aliyun.com/article/1713599
> - OpenClaw SearXNG + DuckDuckGo + Tavily 集成指南（SegmentFault）：https://segmentfault.com/a/1190000047612002
> - OpenClaw 联网工具完全指南（知乎）：https://zhuanlan.zhihu.com/p/2014043504494544090
> - OpenClaw Firecrawl 技能（CSDN）：https://blog.csdn.net/weixin_42538175/article/details/160698680
> - OpenClaw + Claude Code 搜索配置（博客园）：https://www.cnblogs.com/itech/p/19926911
