# OpenClaw 管理宿主机 Claude Code 和 Hermes Agent 指南

> 场景：OpenClaw 运行在 Debian 虚拟机上，需要管理宿主机（或其他远程机器）上的 Claude Code 和 Hermes Agent。

---

## 一、架构概览

```
┌─────────────────────────────────────────────────────────┐
│                    Debian 虚拟机                          │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │              OpenClaw Gateway                │        │
│  │         (主 Agent / 调度中心)                 │        │
│  │                                              │        │
│  │  工具: nodes, sessions_spawn, exec, file_    │        │
│  │       fetch, file_write, cron, message       │        │
│  └───────────┬──────────────┬───────────────────┘        │
│              │              │                            │
│      SSH / Node Pairing     │   sessions_spawn           │
│              │              │   (子代理)                  │
│  ┌───────────▼──────────────▼───────────────────┐        │
│  │               宿主机 (Host)                    │        │
│  │                                              │        │
│  │  ┌──────────────┐    ┌──────────────────┐    │        │
│  │  │ Claude Code  │    │  Hermes Agent     │    │        │
│  │  │ (编码 Agent)  │    │  (自学习 Agent)   │    │        │
│  │  └──────────────┘    └──────────────────┘    │        │
│  └──────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

OpenClaw 提供了 **三种核心机制** 来管理远程 Agent：

| 机制 | 用途 | 适用场景 |
|------|------|---------|
| **Node Pairing（设备配对）** | 将宿主机注册为 OpenClaw 节点，远程执行命令、传输文件 | 长期管理、频繁交互 |
| **SSH + exec** | 通过 SSH 远程执行命令，无需配对 | 临时操作、简单任务 |
| **sessions_spawn（子代理）** | 在 OpenClaw 内部创建隔离的子 Agent 会话执行任务 | 并发任务、专业分工 |

---

## 二、方法一：Node Pairing（设备配对）— 推荐

### 原理

将宿主机注册为 OpenClaw 的 paired node，之后可以通过 `nodes` 工具远程执行命令、拍照、传输文件。

### Step 1：在宿主机上安装 OpenClaw（作为 node）

```bash
# 宿主机上安装 OpenClaw（如果还没装）
curl -fsSL https://claude.ai/install.sh | bash  # 仅安装 CLI
# 或完整安装
npm install -g openclaw
```

### Step 2：在宿主机上启动 Gateway 并获取配对码

```bash
# 宿主机上
openclaw gateway start
openclaw nodes pairing generate
# 输出类似： pairing code: XXXX-XXXX-XXXX
```

### Step 3：在虚拟机 OpenClaw 上配对

使用 `nodes approve` 配对：

```bash
# 在虚拟机 OpenClaw 中
nodes action=approve <pairing-request-id>
```

或在 OpenClaw 控制 UI（WebChat）中操作。

### Step 4：验证配对

```bash
nodes action=status
# 应显示宿主机在线
```

### Step 5：远程执行命令

配对成功后，可以直接在 OpenClaw 中对宿主机执行操作：

```bash
# 在宿主机上执行命令
nodes action=exec command="claude --version" node=<host-node-id>

# 在宿主机上执行多行命令
nodes action=exec command="cd /project && claude '完成这个功能'" node=<host-node-id>
```

### Node 支持的远程操作

| 操作 | 命令示例 |
|------|---------|
| 执行命令 | `nodes action=exec command="..." node=<id>` |
| 截图 | `nodes action=screenshot node=<id>` |
| 拍照 | `nodes action=camera_snap node=<id>` |
| 获取设备信息 | `nodes action=device_info node=<id>` |
| 文件传输 | `file_fetch` / `file_write` |

---

## 三、方法二：SSH + exec（无需配对）

如果不想在宿主机上安装 OpenClaw，可以直接用 SSH 远程执行。

### 前提

- 宿主机 SSH 已开启
- 虚拟机有宿主机的 SSH 密钥

### 直接执行命令

```bash
# 在宿主机上检查 Claude Code 版本
ssh user@host "claude --version"

# 在宿主机上运行 Claude Code 完成编码任务
ssh user@host "cd /path/to/project && claude '实现用户登录功能，写测试并运行'"

# 检查 Hermes Agent 版本
ssh user@host "hermes --version"

# 启动 Hermes Agent
ssh user@host "hermes"

# 在后台运行 Hermes
ssh user@host "nohup hermes gateway > /tmp/hermes.log 2>&1 &"
```

### 传输项目文件

```bash
# 拉取宿主机上的文件到虚拟机
scp user@host:/path/to/file /local/path/

# 推送虚拟机上的文件到宿主机
scp /local/file user@host:/path/to/destination/
```

### 配合 OpenClaw 的 exec 工具

在 OpenClaw 会话中可以直接用 `exec` 执行 SSH 命令：

```bash
# OpenClaw exec 工具
exec command="ssh user@host 'claude --version'" timeout=30
```

---

## 四、方法三：sessions_spawn（子代理）— 最强大

### 原理

OpenClaw 可以创建隔离的子 Agent 会话，每个子 Agent 有自己的上下文、模型和任务。子 Agent 在虚拟机本地运行，但可以通过 SSH 操作宿主机。

### 创建子 Agent 执行远程编码任务

```
# 告诉 OpenClaw：
"派一个子代理去宿主机上运行 Claude Code 完成以下任务：
项目路径：/home/user/my-project
任务：重构 auth 模块，将 JWT 改为 session-based 认证
完成后汇报结果"
```

OpenClaw 内部会调用 `sessions_spawn`：

```
sessions_spawn(
  task="SSH 到宿主机 192.168.31.100，进入 /home/user/my-project，
        运行 Claude Code 完成 JWT 到 session-based 认证的重构，
        完成后汇报改动摘要",
  runtime="subagent",
  mode="run",
  taskName="host-claude-refactor"
)
```

### 并发多任务

同时派多个子 Agent 处理不同任务：

```
# 任务 A：宿主机上用 Claude Code 写新功能
sessions_spawn(
  task="ssh user@host 'cd /project && claude 实现支付模块'",
  taskName="host-payment-feature"
)

# 任务 B：宿主机上用 Hermes 做代码审查
sessions_spawn(
  task="ssh user@host 'cd /project && hermes 对整个项目做代码审查，输出 Markdown 报告'",
  taskName="host-hermes-review"
)

# 任务 C：虚拟机本地做其他事
# ... 主会话继续处理其他任务
```

三个子 Agent 并行执行，互不干扰。

### 检查子 Agent 状态

```
subagents action=list
```

### 等待子 Agent 完成

```
sessions_yield message="等待子代理完成编码任务..."
```

完成后子 Agent 的输出会自动推送到主会话。

---

## 五、方法四：Cron 定时任务自动分配

### 定时在宿主机上执行任务

```bash
# 每天早上 9 点让宿主机上的 Claude Code 做代码审查
cron action=add job={
  "name": "每日代码审查",
  "schedule": {"kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai"},
  "payload": {
    "kind": "agentTurn",
    "message": "SSH 到宿主机，运行 'cd /project && claude 对整个项目做代码审查，生成报告写入 /tmp/review.md'，然后用 file_fetch 拉取报告并推送给我"
  },
  "sessionTarget": "isolated"
}
```

### 定时触发 Hermes 自学习

```bash
# 每周一让 Hermes 回顾上周的工作记录并更新技能
cron action=add job={
  "name": "Hermes 周度学习",
  "schedule": {"kind": "cron", "expr": "0 8 * * 1", "tz": "Asia/Shanghai"},
  "payload": {
    "kind": "agentTurn",
    "message": "SSH 到宿主机，运行 'hermes'，让它回顾最近一周的项目工作记录，提炼新的技能到 skills 目录，完成后汇报"
  },
  "sessionTarget": "isolated"
}
```

---

## 五、实际使用场景

### 场景 1：你发一句话，OpenClaw 调度 Claude Code 干活

```
Aaron：帮我把那个 Python 项目的测试覆盖率提高到 90%
```

OpenClaw 自动：
1. `sessions_spawn` 创建子代理
2. 子代理 `exec ssh user@host "cd /project && claude '将测试覆盖率提高到90%' "`
3. Claude Code 在宿主机上工作
4. 子代理完成后汇报结果

### 场景 2：定时让 Hermes 做项目分析

```
Aaron：每天晚上 10 点让 Hermes 分析项目运行日志
```

设置 cron：
```
cron 每天 22:00 → sessions_spawn → ssh 到宿主机 → hermes 分析日志 → 推送摘要
```

### 场景 3：多 Agent 并行开发

```
Aaron：同时做三件事：
1. Agent A 在宿主机上用 Claude Code 写后端 API
2. Agent B 在宿主机上用 Hermes 整理文档
3. Agent C 在虚拟机上整理文件
```

三个 `sessions_spawn` 并行执行。

---

## 六、四种方案对比

| 方案 | 复杂度 | 实时性 | 并发 | 文件传输 | 适用场景 |
|------|--------|--------|------|---------|---------|
| **Node Pairing** | 中 | ✅ 实时 | ✅ | ✅ 原生支持 | 长期管理、频繁交互 |
| **SSH + exec** | 低 | ✅ 实时 | ✅ | 需要 scp | 临时操作、简单任务 |
| **sessions_spawn** | 中 | ⚠️ 异步 | ✅✅ 强大 | 通过 SSH | 复杂任务、多 Agent 并行 |
| **Cron 定时** | 低 | ❌ 定时 | ✅ | 通过 SSH | 定时自动化任务 |

---

## 七、推荐架构

日常管理用 **Node Pairing + SSH + sessions_spawn** 组合：

```
OpenClaw（虚拟机）
    │
    ├── Node Pairing → 宿主机（长期连接，可随时发命令）
    │
    ├── SSH + exec   → 宿主机（临时操作，快速执行）
    │
    ├── sessions_spawn → 子代理 A → 宿主机 Claude Code（编码任务）
    │                  → 子代理 B → 宿主机 Hermes Agent（分析任务）
    │                  → 子代理 C → 虚拟机本地（其他任务）
    │
    └── Cron 定时     → 每天自动执行常规任务
```

---

## 八、快速配置示例

### 配置 SSH 免密登录（虚拟机 → 宿主机）

```bash
# 虚拟机上生成密钥（如果还没有）
ssh-keygen -t ed25519 -C "openclaw-vm"

# 拷贝公钥到宿主机
ssh-copy-id user@192.168.31.100

# 测试免密登录
ssh user@192.168.31.100 "echo OK"
```

### 配置 OpenClaw SSH 节点（可选）

在 `openclaw.json` 中添加：

```json
{
  "nodes": {
    "host": {
      "host": "192.168.31.100",
      "user": "root",
      "identityFile": "~/.ssh/id_ed25519"
    }
  }
}
```

---

## 九、实用命令速查

```bash
# === SSH 方式 ===
# 宿主机运行 Claude Code 一次性任务
ssh user@host "cd /project && claude '任务描述'"

# 宿主机后台运行 Hermes
ssh user@host "nohup hermes gateway > /tmp/hermes.log 2>&1 &"

# 检查宿主机 Hermes 是否在运行
ssh user@host "ps aux | grep hermes"

# === Node Pairing 方式 ===
# 检查节点状态
nodes action=status

# 远程执行
nodes action=exec command="claude --version" node=host

# 截图
nodes action=screenshot node=host
```

---

*信息来源：OpenClaw 本地文档（/usr/lib/node_modules/openclaw/docs/）、OpenClaw GitHub README（2026.5.27 版本）、MindStudio.ai 的多 Agent 对比文章、Reddit 社区讨论、Medium ClaudeClaw 架构分析文章。*
