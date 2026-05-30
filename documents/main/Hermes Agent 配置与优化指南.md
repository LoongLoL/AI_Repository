# Hermes Agent 配置与优化指南

> 虾仁 🦅 为 Aaron 整理 | 2026-05-30
> 基于 Hermes Agent 官方文档 v2.1.0 + 当前实际配置

---

## 一、安装后必做配置（刚装完就做）

### 1.1 运行 Setup Wizard

```bash
hermes setup --portal
```

**为什么先做这个？** 一个 OAuth 搞定模型 + 所有 Tool Gateway 工具（web search、image generation、TTS、browser）。比一个个配 API Key 快得多。

### 1.2 检查系统健康

```bash
hermes doctor
```

这会检查：依赖是否完整、配置是否正确、模型是否连通。发现红色警告就修。

### 1.3 验证当前模型

```bash
hermes config          # 看当前配置
hermes model           # 交互式切换模型
```

**当前你的配置：**
- 主模型: `openrouter/owl-alpha`（免费）
- 备用: `nvidia/nemotron-3-super-120b-a12b:free` → `deepseek/deepseek-v4-flash` → `google/gemini-2.0-flash-001:free`
- 提供商: OpenRouter + DeepSeek

### 1.4 开启自动更新

```bash
hermes config set updates.pre_update_backup true
hermes config set updates.backup_keep 5
```

---

## 二、性能优化（关键配置项）

### 2.1 上下文压缩 — 省钱省 token 的核心

```bash
hermes config set compression.enabled true       # 已开启
hermes config set compression.threshold 0.60      # 默认0.5，调到0.6晚点压缩更省API调用
hermes config set compression.target_ratio 0.25   # 压缩到25%，保留更多信息
```

**当前值：** threshold=0.5, target_ratio=0.2, protect_last_n=20

**调优建议：**
- 长对话场景（写代码、多轮分析）：threshold 调到 0.6-0.7，避免频繁压缩打断思路
- 短问答场景：保持 0.5 即可
- `protect_last_n: 20` — 保护最近20条消息不被压缩，够用

### 2.2 Prompt Caching — 减少重复 token 计费

```bash
hermes config set prompt_caching.cache_ttl 5m     # 当前值，一般不用改
hermes config set openrouter.response_cache true  # 已开启
hermes config set openrouter.response_cache_ttl 300
```

### 2.3 工具输出限制 — 防止上下文爆炸

```bash
hermes config set tool_output.max_bytes 50000     # 单工具输出上限
hermes config set tool_output.max_lines 2000       # 最大行数
hermes config set tool_output.max_line_length 2000  # 单行最大长度
```

**如果经常处理大文件：**
```bash
hermes config set file_read_max_chars 200000  # 从10万提到20万
```

### 2.4 最大对话轮次

```bash
hermes config set agent.max_turns 120    # 默认90，复杂任务提到120
hermes config set agent.api_max_retries 3  # API失败重试次数
```

### 2.5 超时配置

```bash
hermes config set terminal.timeout 300         # 命令执行超时（秒）
hermes config set agent.gateway_timeout 3600    # 网关超时从1800提大
hermes config set agent.clarify_timeout 600     # 澄清超时
```

---

## 三、多模型/多 Provider 策略

### 3.1 为什么要配多个模型？

- **主模型（强但贵/限流）** → 处理复杂推理
- **备用模型（免费/快）** → 主模型挂了自动切换
- **视觉模型** → 专门处理图片
- **辅助模型** → 压缩、搜索、审核等后台任务

### 3.2 配置备用模型（Fallback）

当前你已有 fallbacks，但建议优化：

```yaml
model:
  primary: openrouter/owl-alpha
  fallbacks:
  - deepseek/deepseek-v4-flash        # 便宜又快，优先切换
  - nvidia/nemotron-3-super-120b-a12b:free  # 免费超大模型
  - google/gemini-2.0-flash-001:free  # Google免费模型
```

修改方式：
```bash
hermes config edit   # 直接编辑 config.yaml
```

### 3.3 Credential Pool（多 Key 轮转）

如果你有同一个提供商的多个 API Key：

```bash
hermes auth add openrouter    # 添加第一个 Key
hermes auth add openrouter    # 添加第二个 Key（自动轮转）
hermes auth list              # 查看已配置的凭据
```

好处：一个 Key 限流了自动换下一个，不会中断工作。

### 3.4 Auxiliary Models（辅助任务专用）

```bash
# 视觉任务专用模型（你配了 google/gemma-4-31b-it:free）
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.vision.model google/gemma-4-31b-it:free

# 压缩任务用小模型
hermes config set auxiliary.compression.provider openrouter
hermes config set auxiliary.compression.model google/gemini-2.0-flash-001:free
```

---

## 四、Memory 系统优化

### 4.1 当前状态

```
memory_enabled: true          ✓ 已开启
user_profile_enabled: true    ✓ 已开启
memory_char_limit: 2200       ← 可适当提到 3000
user_char_limit: 1375         ← 可提到 2000
```

### 4.2 优化建议

```bash
# 增加记忆容量
hermes config set memory.memory_char_limit 3000
hermes config set memory.user_char_limit 2000

# 调整记忆触发频率（默认每10轮触发一次 nudge）
hermes config set memory.nudge_interval 8

# flush_min_turns 控制至少多少轮才写入（默认6）
hermes config set memory.flush_min_turns 5
```

### 4.3 记忆清理

- 定期清理过时记忆：直接编辑 `~/.hermes/memories/MEMORY.md`
- 原则：只保留**跨会话有长期价值**的信息
- 不保留：临时任务进度、文件计数、PR 号等会过期的内容

---

## 五、Skills 系统优化

### 5.1 Skill 安装

```bash
# 搜索 skill
hermes skills search "python"
hermes skills browse    # 浏览所有可用 skill

# 安装 skill
hermes skills install <ID>

# 检查更新
hermes skills check
hermes skills update
```

### 5.2 外部 Skill 目录

```bash
hermes config set skills.external_dirs '["/path/to/skills"]'
```

### 5.3 Skill 管理最佳实践

- **常用 skill 保持更新**：`hermes skills update`
- **不用的 skill 别装太多**：每个 skill 都占 context 空间
- **自己写 skill**：遇到重复性任务，让虾仁帮你写成 skill

---

## 六、Cron 定时任务系统

### 6.1 创建定时任务

```bash
# 每天早7:50执行
hermes cron create "0 7 * * *" --prompt "收集今天的AI新闻"

# 每30分钟执行
hermes cron create "30m" --prompt "检查系统状态"

# 一次性任务
hermes cron create "2026-05-31T10:00:00" --prompt "提醒：提交周报"
```

### 6.2 当前已有定时任务

你的系统已配置 `每日新闻采集`（7:50 Asia/Shanghai），三个栏目：
- 🌏 国际 AI/科技
- 🇨🇳 国内 AI/科技
- 🇨🇳 国内时事

---

## 七、Gateway（消息平台）配置

### 7.1 支持的通道

已连接：**QQ Bot** 
还支持：Telegram、Discord、Slack、WhatsApp、Signal、Matrix 等

### 7.2 当前 QQ Bot 注意事项

- 使用 `hermes gateway setup` 配置
- delivery 模式用 `origin`（不要用 `announce`，qqbot 格式不支持）
- 定时任务推送由 heartbeat 接管

### 7.3 Gateway 服务管理

```bash
hermes gateway status    # 查看状态
hermes gateway restart   # 重启
hermes gateway start     # 启动
hermes gateway stop      # 停止
```

---

## 八、安全配置

### 8.1 当前安全设置

```
redact_secrets: true      ✓ 密钥自动脱敏
tirith_enabled: true      ✓ 安全扫描开启
approvals.mode: manual    ← 每次破坏性命令都确认
```

### 8.2 推荐调优

```bash
# 如果你信任环境，可以改成 smart 模式（低风险自动放行）
hermes config set approvals.mode smart

# 或者完全关闭（不推荐）
hermes config set approvals.mode off
```

**Aaron 的建议：** 保持 `manual` 或 `smart`，安全第一。

---

## 九、实用 Slash 命令速查

### 日常高频

| 命令 | 作用 |
|------|------|
| `/new` | 开新会话 |
| `/model` | 查看/切换模型 |
| `/skill <name>` | 加载 skill |
| `/tools` | 管理工具 |
| `/cron` | 管理定时任务 |
| `/compress` | 手动压缩上下文 |

### 效率提升

| 命令 | 作用 |
|------|------|
| `/verbose` | 循环切换详细程度 |
| `/fast` | 切换优先/快速处理 |
| `/background <prompt>` | 后台运行任务 |
| `/queue <prompt>` | 排队到下一轮 |
| `/steer <prompt>` | 下一轮工具调用后注入指令 |
| `/yolo` | 跳过危险命令确认 |

### 查询类

| 命令 | 作用 |
|------|------|
| `/context` | 查看上下文使用情况 |
| `/usage` | Token 用量 |
| `/goal` | 设置长期目标 |
| `/agents` | 查看活跃 agent |

---

## 十、多 Agent 协作

### 10.1 delegate_task（轻量）

适合分钟级子任务：

```
delegate_task(
  goal="分析这个Python项目的代码质量",
  context="项目在 /root/projects/myapp",
  toolsets=["terminal", "file"]
)
```

- 最多3个并发子任务
- 子任务不能再次委托（max_spawn_depth=1）
- 父会话中断则子任务取消

### 10.2 tmux 多 Agent（重量）

适合需要交互的长时间任务：

```bash
# 启动一个独立 agent
tmux new-session -d -s worker1 -x 120 -y 40 'hermes'

# 发送任务
sleep 8 && tmux send-keys -t worker1 '帮我重构 auth 模块' Enter

# 查看进度
tmux capture-pane -t worker1 -p | tail -30
```

### 10.3 Cron Job（持久）

适合定时执行的后台工作，不怕会话中断。

---

## 十一、当前配置诊断 & 改进建议

### 你的系统现状

| 项目 | 当前值 | 建议 |
|------|--------|------|
| 主模型 | owl-alpha（免费） | ✓ 够用 |
| 备用模型 | 3个免费 + DeepSeek | ✓ 覆盖全面 |
| 压缩 | 已开启 | 可微调 threshold |
| Memory | 已开启 | 可增大 char_limit |
| 安全检查 | 已开启 | ✓ 保持 |
| 自动备份 | pre_update_backup=false | 建议开启 |
| Checkpoints | enabled=false | 建议开启（代码工作时） |
| 时区 | 未设置 | 建议设 Asia/Shanghai |

### 立即可做的改进

```bash
# 1. 开启更新前备份
hermes config set updates.pre_update_backup true

# 2. 开启 checkpoints（代码操作可回滚）
hermes config set checkpoints.enabled true

# 3. 设时区
hermes config set timezone Asia/Shanghai

# 4. 增大记忆容量
hermes config set memory.memory_char_limit 3000
hermes config set memory.user_char_limit 2000

# 5. 优化压缩参数
hermes config set compression.threshold 0.6
hermes config set compression.target_ratio 0.25

# 6. 延时自动重置（当前1440分钟=24小时，可以）
# session_reset.idle_minutes 保持即可
```

---

## 十二、故障排查速查

| 问题 | 解决 |
|------|------|
| 命令没反应 | `/restart`（网关）或重开终端 |
| 模型连不上 | `hermes doctor` → 检查 `.env` → `hermes auth list` |
| 工具不见了 | `hermes tools` → `/reset` 新会话 |
| 配置改了不生效 | 网关要 `/restart`，CLI 要重开 |
| 内存/磁盘满 | `hermes sessions prune --older-than 30` |
| Gateway 崩溃 | `systemctl --user reset-failed hermes-gateway` |
| 子代理卡住 | `/stop` + `/new` |

---

## 参考链接

- 官方文档: https://hermes-agent.nousresearch.com/docs
- GitHub: https://github.com/NousResearch/hermes-agent
- Discord: https://discord.gg/hermes-agent
- Skills 市场: https://hermes-agent.nousresearch.com/docs/reference/skills-catalog

---

> 📌 **Aaron 快速上手路线：**
> 1. `hermes setup --portal` — 一次性搞定认证
> 2. `hermes doctor` — 体检
> 3. 套用上面"立即可做的改进"的 6 条命令
> 4. 开始用，遇到问题查"故障排查速查"
> 5. 常用操作让虾仁写成 skill，越用越顺手
