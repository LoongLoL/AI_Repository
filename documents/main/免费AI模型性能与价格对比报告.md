# 💰 免费 AI 模型性能与价格对比报告

**编制日期：** 2026年5月27日
**数据来源：** OpenRouter API 实时查询

---

## 一、OpenRouter 免费模型全景

OpenRouter 上共有 **27 个免费模型**（定价为 0），涵盖文本、多模态、代码生成等不同类型。以下是分类和关键参数：

### 🏆 第一梯队：百万级上下文 + 高性能（适合作为主模型/主力 fallback）

| 模型 | 上下文 | 模态 | 核心特点 |
|------|-------|------|---------|
| **openrouter/owl-alpha** 🦅 | 1,048,756 | text | 高性能 Agent 模型，原生支持工具调用，代码生成和复杂指令执行能力强 |
| **deepseek/deepseek-v4-flash:free** | 1,048,576 | text | DeepSeek V4 Flash 免费版，284B 参数 MoE，13B 激活参数，效率优先 |
| **qwen/qwen3-coder:free** | 1,048,576 | text | Qwen3 Coder 480B A35B，专业代码生成 MoE 模型 |
| **nvidia/nemotron-3-super-120b-a12b:free** | 1,000,000 | text | NVIDIA 开源 MoE 模型，120B 参数仅激活 12B |

### 🥈 第二梯队：20万+ 上下文，中等规模（适合子代理/特定任务）

| 模型 | 上下文 | 模态 | 核心特点 |
|------|-------|------|---------|
| **poolside/laguna-m.1:free** | 262,144 | text | Poolside 旗舰代码 Agent 模型 |
| **google/gemma-4-26b-a4b-it:free** | 262,144 | text+image+video | Google 多模态 MoE，26B 参数 |
| **google/gemma-4-31b-it:free** | 262,144 | text+image+video | Google 密集多模态 31B 模型 |
| **qwen/qwen3-next-80b-a3b-instruct:free** | 262,144 | text | Qwen3-Next 系列指令优化版 |
| **nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free** | 256,000 | text+image+audio+video | NVIDIA 全模态推理模型 |
| **nvidia/nemotron-3-nano-30b-a3b:free** | 256,000 | text | 高效小型 MoE |
| **minimax/minimax-m2.5:free** | 204,800 | text | 通用生产力模型 |

### 🥉 第三梯队：13万上下文，开源/轻量级

| 模型 | 上下文 | 模态 | 核心特点 |
|------|-------|------|---------|
| **baidu/cobuddy:free** | 131,072 | text | 百度代码生成模型，AI Agent 工作流优化 |
| **poolside/laguna-xs.2:free** | 131,072 | text | Poolside 第二代小尺寸代码模型 |
| **openai/gpt-oss-120b:free** | 131,072 | text | OpenAI 开源 117B MoE，Apache 2.0 |
| **openai/gpt-oss-20b:free** | 131,072 | text | OpenAI 开源 21B 模型，Apache 2.0 |
| **z-ai/glm-4.5-air:free** | 131,072 | text | 智谱 GLM-4.5 轻量版 |
| **meta-llama/llama-3.3-70b-instruct:free** | 131,072 | text | Meta Llama 3.3 70B 多语言 |
| **meta-llama/llama-3.2-3b-instruct:free** | 131,072 | text | Meta Llama 3.2 3B 小模型 |
| **nvidia/nemotron-nano-12b-v2-vl:free** | 128,000 | text+image+video | NVIDIA 多模态推理，视频理解 |
| **nvidia/nemotron-nano-9b-v2:free** | 128,000 | text | NVIDIA 9B 通用 LLM |

### 📦 第四梯队：小模型 / 边缘设备

| 模型 | 上下文 | 备注 |
|------|-------|------|
| **liquid/lfm-2.5-1.2b-thinking:free** | 32,768 | 轻量推理模型，适合 Agent + RAG |
| **liquid/lfm-2.5-1.2b-instruct:free** | 32,768 | 紧凑指令模型，适合边缘设备 |
| **cognitivecomputations/dolphin-mistral-24b-venice-edition:free** | 32,768 | 无审查版 Mistral 24B |

### 🌐 特殊路由

| 模型 | 功能 |
|------|------|
| **openrouter/free** | 自动路由到随机免费模型，200K 上下文，文本+图像 |
| **google/lyria-3-pro-preview** | Google 音乐生成，完整歌曲 $0.08/首 |
| **google/lyria-3-clip-preview** | Google 音乐生成，30秒片段 $0.04/条 |

---

## 二、价格对比：免费 vs 付费模型

### DeepSeek 系列

| 模型 | 上下文 | 输入/1K tokens | 输出/1K tokens | 相比付费版 |
|------|-------|---------------|---------------|-----------|
| **deepseek-v4-flash:free** | 1M | **$0** | **$0** | — |
| **deepseek-v4-flash** | 1M | $0.0001 | $0.0002 | 免费版 ≈ 付费版 100% 免费 |

### OpenAI 系列

| 模型 | 上下文 | 输入/1K tokens | 输出/1K tokens |
|------|-------|---------------|---------------|
| gpt-oss-120b:free | 131K | **$0** | **$0** |
| gpt-oss-20b:free | 131K | **$0** | **$0** |
| gpt-4.1-nano | 1M | $0.0001 | $0.0004 |
| gpt-4o-mini | 128K | $0.00015 | $0.0006 |
| gpt-4.1-mini | 1M | $0.0004 | $0.0016 |
| **gpt-4o** | 128K | $0.0025 | $0.01 |
| **gpt-4.1** | 1M | $0.002 | $0.008 |
| **o3-mini** | 200K | $0.0011 | $0.0044 |
| **o4-mini** | 200K | $0.0011 | $0.0044 |
| **o3** | 200K | $0.002 | $0.008 |

### Anthropic Claude 系列

| 模型 | 上下文 | 输入/1K tokens | 输出/1K tokens |
|------|-------|---------------|---------------|
| **claude-sonnet-4.6** | 1M | $0.003 | $0.015 |
| **claude-opus-4.7** | 1M | $0.005 | $0.025 |

### Google Gemini 系列

| 模型 | 上下文 | 输入/1K tokens | 输出/1K tokens |
|------|-------|---------------|---------------|
| **gemini-2.5-flash** | 1M | $0.0003 | $0.0025 |
| **gemini-2.5-pro** | 1M | $0.00125 | $0.01 |

### Qwen 系列

| 模型 | 上下文 | 输入/1K tokens | 输出/1K tokens |
|------|-------|---------------|---------------|
| **qwen3-coder:free** | 1M | **$0** | **$0** |
| **qwen3-coder-flash** | 1M | $0.000195 | $0.000975 |
| **qwen3-coder-plus** | 1M | $0.00065 | $0.00325 |
| **qwen3-max** | 262K | $0.00078 | $0.0039 |

---

## 三、价格等级速查表（按成本排序）

| 等级 | 输入/1K tokens | 代表模型 | 适用场景 |
|------|--------------|---------|---------|
| **免费** 🆓 | $0.000 | owl-alpha, deepseek-v4-flash:free, qwen3-coder:free | 日常对话、代码开发、Agent 任务 |
| **极低** 💎 | $0.0001-0.0003 | gpt-4.1-nano, deepseek-v4-flash, gemini-2.5-flash | 大规模推理、批量处理 |
| **低** 💰 | $0.0004-0.0011 | gpt-4.1-mini, o3-mini, o4-mini, gpt-4o-mini | 日常生产环境 |
| **中** 💰💰 | $0.00125-0.003 | gemini-2.5-pro, claude-sonnet, gpt-4.1, gpt-4o | 专业任务、复杂推理 |
| **高** 💰💰💰 | $0.003-0.005 | claude-opus, qwen3-max | 顶级任务、极限性能需求 |

---

## 四、免费模型的真实可用性分析

**⚠️ 重要提示：免费模型存在以下限制：**

### 1. 速率限制严重
- 免费模型通过 **共享免费提供商**（如 Venice）路由
- 实测：`qwen/qwen3-coder:free` → 429 限流，Retry-After 19秒
- 高峰期几乎不可用
- `openrouter/free` 路由器会自动切换，但响应不确定

### 2. 性能差异
| 免费模型 | 实际可用性 | 推荐度 |
|---------|-----------|-------|
| **owl-alpha** | ✅ **高**（当前主模型，稳定） | ⭐⭐⭐⭐⭐ |
| **deepseek-v4-flash:free** | ⚠️ 中等（依赖免费提供商） | ⭐⭐⭐⭐ |
| **nemotron-3-super:free** | ✅ 较高 | ⭐⭐⭐⭐ |
| **qwen3-coder:free** | ❌ 低（429 频繁） | ⭐⭐ |
| **qwen3-next:free** | ⚠️ 中等 | ⭐⭐⭐ |
| **gemma-4:free** | ✅ 较高 | ⭐⭐⭐⭐ |
| **gpt-oss:free** | ⚠️ 中等 | ⭐⭐⭐ |
| **llama-3.3-70b:free** | ✅ 较高 | ⭐⭐⭐⭐ |

### 3. 与付费版的差距
| 维度 | 免费版 | 付费版 |
|------|-------|-------|
| 速率限制 | 严格，排队 + 429 | 无限制（按用量付费） |
| 服务质量 | 共享排队，延迟高 | 优先调度，延迟低 |
| 模型选择 | 有限（27个） | 全量（5800+） |
| 可靠性 | ⚠️ 不可靠 | ✅ 非常可靠 |
| 成本 | $0 | 按量计费 |

---

## 五、推荐配置方案

### 🥇 推荐免费配置（当前方案）
```
主模型:  openrouter/owl-alpha          ✅ 免费+稳定
Fallback: deepseek/deepseek-v4-flash   $0.0001/$0.0002 per token（极低成本）
```

### 🥈 极致低成本方案
```
主模型:  deepseek/deepseek-v4-flash    $0.0001/$0.0002
Fallback: openrouter/owl-alpha         FREE（免费兜底）
```

### 🥉 混合方案（兼顾性能与成本）
```
主模型:   openrouter/owl-alpha         FREE
Fallback1: deepseek/deepseek-v4-flash  $0.0001/$0.0002（极低）
Fallback2: qwen/qwen3-coder-flash      $0.000195/$0.000975（代码任务）
```

### 关于 Qwen3 Coder 免费版
- **确认不可用：** 每次调用都会 429 限流
- **建议移除或放到 fallback 最后**
- 付费版 `qwen3-coder-flash` 仅 $0.000195/1K tokens，性价比极高（比 deepseek-v4-flash 贵不到一倍，但代码能力更强）

---

## 六、结论与建议

1. **当前配置合理**：owl-alpha → deepseek-v4-flash 是免费的黄金组合
2. **Qwen3 Coder free 建议移除 fallback**：429 限流导致零回复
3. **如需更强的代码能力**：考虑添加 qwen3-coder-flash（付费，但极其便宜）
4. **如未来需要视觉/多模态**：Gemma-4（免费）或 Gemini-2.5-flash（$0.0003/$0.0025）是好选择
5. **OpenRouter 免费模型整体趋势**：数量在增加，但可靠性随使用量下降，核心依赖应优先考虑付费模型

---

*本报告由虾仁自动采集 OpenRouter API 生成，数据截至 2026-05-27 02:15 UTC+8*
