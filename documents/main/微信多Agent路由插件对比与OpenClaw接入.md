# 微信多Agent路由插件对比与OpenClaw接入指南

## 一、场景说明

**现状：** Hermes Agent 已接入微信
**目标：** OpenClaw 也接入微信（两个Agent都能通过微信对话）

**核心限制：** 一个微信号只能绑定一个 Agent 通道，所以必须在路由层做分发。

---

## 二、可行方案对比

### 方案A：weixin-agent-sdk 多实例（推荐）

> GitHub：`https://github.com/wong2/weixin-agent-sdk`（2.3k ⭐）

**原理：** 启动两个独立的 `weixin-acp` 实例，分别连接 Hermes 和 OpenClaw

```
微信用户 → 微信号A → weixin-acp → Hermes Agent
         → 微信号B → weixin-acp → OpenClaw
```

**缺点：** 需要两个微信号，一个号绑 Hermes，一个号绑 OpenClaw
**优点：** 最稳定，两个 Agent 完全独立

```bash
# 终端1：Hermes（现有）
npx weixin-acp start -- hermes

# 终端2：OpenClaw（新增）
npx weixin-acp start -- openclaw
```

---

### 方案B：clawcenter（推荐，单微信号）

> GitHub：`https://github.com/ruihanglix/clawcenter`

**原理：** 中央路由器，用**话题标签**（`#标签`）切换不同 Agent

```
微信 → clawcenter（路由层）→ #openclaw OpenClaw
                         → #hermes  Hermes Agent
```

**使用方式（在微信里发消息）：**
```
#openclaw 帮我整理一下今天的日程
#hermes  帮我搜一下最新的AI新闻
#code    帮我写一个Python爬虫
```

**优点：** 只需一个微信号，通过标签智能路由到对应 Agent
**缺点：** 需要在消息前加标签，不如自然对话流畅

---

### 方案C：weixin-agent-gateway

> GitHub：`https://github.com/BytePioneer-AI/weixin-agent-gateway`

**原理：** 面向微信入口的多后端AI网关，解耦微信接入层与后端路由层

```
微信 → weixin-agent-gateway → OpenClaw 后端
                           → Hermes 后端
                           → Codex / Claude Code 后端
```

**优点：** 架构清晰，支持多后端同时运行
**缺点：** 新项目，文档和社区较少

---

### 方案D：weixin-agent（duo121）

> GitHub：`https://github.com/duo121/weixin-agent`

**原理：** 全局 Router + 多个本地 AI 终端会话

```
微信 → weixin-agent Router → Agent会话A
                          → Agent会话B
                          → Agent会话C
```

**优点：** AI-native 设计，支持 Agent 间转交 Ticket
**缺点：** 没有 OpenClaw/Hermes 内置支持，需要自己适配

---

### 方案E：在 OpenClaw 内调用 Hermes（最简单）

**原理：** 只保留 OpenClaw 接微信，需要 Hermes 能力时通过 OpenClaw 的 `sessions_spawn` 或 `exec` 调用 Hermes CLI

```bash
# 在 OpenClaw 对话中：
"用 Hermes 帮我做 xxx"
→ OpenClaw 调用 `hermes run --message "xxx"`
→ 返回结果
```

**优点：** 零改动，不需要额外插件
**缺点：** 不是真正的双 Agent 并行

---

## 三、推荐方案：方案B（clawcenter）

如果你的核心诉求是**一个微信号同时使用两个 Agent**，`clawcenter` 是最匹配的方案。

### 接入步骤

#### 第1步：安装 clawcenter

```bash
# 克隆项目
git clone https://github.com/ruihanglix/clawcenter.git
cd clawcenter

# 安装依赖
npm install
```

#### 第2步：配置后端 Agent

在配置文件中添加 OpenClaw 和 Hermes 作为后端：

```yaml
# config.yaml（示例）
routers:
  - tag: openclaw
    backend: openclaw
    command: "openclaw"
  - tag: hermes
    backend: hermes
    command: "hermes"
```

#### 第3步：启动服务

```bash
npm start
```

#### 第4步：微信对话

```
你：#openclaw 查看今天的日程
OpenClaw：今天你有3个会议...

你：#hermes 搜一下最新AI新闻
Hermes：今天AI领域发生了...
```

---

## 四、如果你愿意用双微信号

建议直接用 `weixin-agent-sdk`：

```bash
# 1. 安装 SDK
npm install -g wong2/weixin-agent-sdk

# 2. 登录第一个微信号（Hermes 用）
npx weixin-acp login
npx weixin-acp start -- hermes

# 3. 登录第二个微信号（OpenClaw 用）
npx weixin-acp login --port 9801
npx weixin-acp start --port 9801 -- openclaw
```

---

## 五、总结

| 方案 | 微信号需求 | 架构复杂度 | 推荐度 |
|------|-----------|-----------|--------|
| **clawcenter** | 1个 | 中 | ⭐⭐⭐⭐⭐ |
| **weixin-agent-sdk 双实例** | 2个 | 低 | ⭐⭐⭐⭐ |
| **weixin-agent-gateway** | 1个 | 中高 | ⭐⭐⭐ |
| **weixin-agent (duo121)** | 1个 | 中 | ⭐⭐ |
| **OpenClaw 内调用 Hermes** | 1个 | 最低 | ⭐⭐⭐ |

**对你最推荐的路径：**
1. 如果想要一个微信号搞定 → 用 **clawcenter**
2. 如果有两个微信号 → 用 **weixin-agent-sdk** 双实例
3. 如果不想折腾 → 保持 Hermes 接微信，**在 OpenClaw 里通过 exec 调用 Hermes**
