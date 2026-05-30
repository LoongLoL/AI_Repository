# Agent Skill 编写规范

> 📅 整理日期：2026-05-30
> 📖 来源：agentskills.io 官方标准、Anthropic 官方文档、OpenClaw 文档、Claude API 最佳实践
> 🎯 适用范围：OpenClaw / Claude Code / Hermes Agent 等兼容 Agent Skills 标准的平台

---

## 一、Skill 是什么

Agent Skills 是一种**开放的、标准化的能力包格式**，让 AI Agent 可以按需加载专业知识和工作流程。

**核心理念**：一个 Skill = 一个文件夹 + 一个 `SKILL.md` 文件。平时不占上下文，需要时自动触发加载。

**三阶段加载机制（Progressive Disclosure）**：
| 阶段 | 内容 | Token 消耗 |
|------|------|-----------|
| **Discovery（发现）** | Agent 启动时仅读取 `name` + `description` | 极低 |
| **Activation（激活）** | 用户任务匹配 `description` 时，读取完整 SKILL.md 到上下文 | 中等 |
| **Execution（执行）** | Agent 按 SKILL.md 中的指令执行任务 | 按需 |

---

## 二、目录结构

```
my-skill/
├── SKILL.md          ← 必需：元数据 + 指令
├── scripts/          ← 可选：可执行脚本
├── references/       ← 可选：参考资料/模板
├── assets/           ← 可选：文件、图片等资源
└── ...               ← 任意额外文件
```

---

## 三、SKILL.md 结构

每个 SKILL.md 由两部分组成：

### 3.1 YAML Frontmatter（必需）

```yaml
---
name: your-skill-name
description: "一句话描述 Skill 的用途和触发条件"
allowed-tools:
  - read
  - write
  - exec
metadata:
  openclaw:
    os: ["linux"]              # 可选：OS 过滤
    requires:
      bins: ["git", "curl"]    # 可选：依赖的二进制工具
      config: ["api_key"]      # 可选：依赖的配置键
---
```

**字段说明**：

| 字段 | 必填 | 限制 | 说明 |
|------|------|------|------|
| `name` | ✅ | 最大 64 字符，仅小写字母/数字/连字符 | 唯一标识符，与文件夹名一致 |
| `description` | ✅ | 最大 1024 字符，非空 | Agent 判断是否触发的唯一依据 |
| `allowed-tools` | 否 | 工具 ID 列表 | 限制该 Skill 可使用的工具 |
| `metadata` | 否 | 键值对 | 平台特定的元数据（OS 过滤、依赖声明等） |

### 3.2 Markdown 正文（必需）

```markdown
# Skill 标题

## 触发条件
描述何时应该使用此 Skill。

## 工作流程
1. 第一步
2. 第二步
3. 第三步

## 注意事项
- 重要约束
- 错误处理方式

## 输出格式
描述期望的输出格式。
```

---

## 四、description 写作规范（最关键）

`description` 是 Agent 判断是否使用此 Skill 的**唯一依据**，写好了 Skill 才对，写不好等于没有。

### ✅ 好的 description：

```yaml
description: "Processes Excel files and generates reports. Use when the user asks to analyze, summarize, or visualize spreadsheet data."
#                  ^^^^^ 做什么                 ^^^^^ 何时触发
```

```yaml
description: "将选择题答案标注到试卷 PDF 上。适用于 PDF 文档答案标记、答题卡批改、mark scheme 标注任务。"
```

### ❌ 差的 description：

```yaml
description: "A tool for data stuff"
# 太模糊，Agent 无法判断何时使用
```

```yaml
description: "I can help you process Excel files"
# 第一人称，Agent 读取时会产生视角混乱
```

**写作要点**：
1. **用第三人称**，避免 "I can..." / "You should..."
2. **既说清楚做什么**，也说清楚**何时触发**
3. **包含关键词**：触发场景中的高频词汇
4. **中文场景可以写中文**，但英文触发率更稳定
5. **一行足够**，不要写成段落

---

## 五、正文写作最佳实践

### 5.1 清晰的结构

```markdown
# Skill 名称

## 触发条件
明确列出 Agent 应该在什么场景下激活此 Skill。

## 工作流程
按步骤列出操作流程：
1. **提取答案**：用 `exec` 跑 pdfplumber 从答案卷提取所有选择题答案
2. **分析试卷**：用 `read` 以图片查看试卷 PDF 结构
3. **标注**：使用方法 XXX 在每题选项旁添加红色答案标注
4. **输出**：生成 `xxx-annotated.pdf`

## 输入
- 答案卷 PDF 文件路径
- 题目卷 PDF 文件路径

## 输出
- 标注后的 PDF 文件
- 文件服务器的预览链接（格式：`http://IP:端口/preview/xxx`）

## 注意事项
- **务必先预览试卷结构再标注**，不要盲目执行
- 答案卷格式不一致时，优先用 pdfplumber 文字提取，降级用逐页 OCR
- 生成的标注 PDF 提供下载链接

## 错误处理
- 如果 pdfplumber 提取失败，改用 OCR
- 如果链接验证失败，丢弃该条换替补
```

### 5.2 内容精简原则

- **SKILL.md 主体建议 500 行以内**，超过则拆分到 `references/`
- **只写"做什么"**，不要写"你是一个有帮助的助手"这类废话
- **指令要可执行**，Agent 读完就知道怎么做
- 用 `# ## ###` 标题层级组织内容，方便 Agent 快速定位

### 5.3 渐进式披露（大文件的组织方式）

当 Skill 内容较多时，使用分层加载：

```
big-skill/
├── SKILL.md              ← 核心指令（始终加载）
├── references/
│   ├── api-reference.md  ← API 文档（按需加载）
│   └── troubleshooting.md ← 故障排除（出错时加载）
├── scripts/
│   └── helper.py         ← 辅助脚本（执行时加载）
└── assets/
    └── template.xlsx     ← 模板文件（生成时加载）
```

在 SKILL.md 中引用：
```markdown
详细 API 参考见 `references/api-reference.md`。
常见问题排查见 `references/troubleshooting.md`。
```

---

## 六、Skill 存放位置（OpenClaw）

| 位置 | 优先级 | 范围 |
|------|--------|------|
| `<workspace>/skills/` | 最高 | 每个 Agent |
| `<workspace>/.agents/skills/` | 高 | 每个工作区 Agent |
| `~/.agents/skills/` | 中 | 共享 Agent 配置 |
| `~/.openclaw/skills/` | 中 | 共享（所有 Agent） |
| 内置（随 OpenClaw 提供） | 低 | 全局 |
| `skills.load.extraDirs` | 最低 | 自定义共享文件夹 |

---

## 七、Skill 命名规范

- 使用 **连字符命名（kebab-case）**：`answer-marker`、`pdf`、`git-commit`
- **推荐动词或动名词**：`summarize-changes`、`deploy-staging`、`review-pr`
- 避免状态型名称（`api-docs`、`team-info`），触发率不如动作型
- 与文件夹名保持一致

---

## 八、常见模式

### 8.1 模板模式（Template Pattern）

适用于有固定输出格式的任务：

```markdown
## 输出格式
```markdown
# 标题

## 板块
1. **条目** — 简要说明
   🔗 来源：[来源名](链接) （已验证）
```
```

### 8.2 工作流模式（Conditional Workflow Pattern）

适用于有分支逻辑的任务：

```markdown
## 工作流程
1. 检查输入类型：
   - 如果是 PDF → 执行路径 A
   - 如果是 DOCX → 执行路径 B
2. 验证结果：
   - 验证通过 → 输出
   - 验证失败 → 回到步骤 1 尝试降级方案
```

### 8.3 MCP 组合模式

```markdown
## 前置条件
此 Skill 需要 MCP Server `xxx` 已配置。
检查方式：调用 `mcp__xxx__check` 确认连接正常。
```

---

## 九、反模式（避免踩坑）

| ❌ 反模式 | ✅ 正确做法 |
|----------|-----------|
| description 太长（超过 1024 字符） | 一行说清做什么+何时触发 |
| 用第一/第二人称写 description | 用第三人称 |
| SKILL.md 超过 1000 行不拆分 | 大文件拆到 `references/` |
| 一个 Skill 做 3 件不相关的事 | 拆成 3 个独立 Skill |
| 没有错误处理说明 | 每种异常都有明确处理指令 |
| description 写得太模糊 | 包含具体触发关键词 |
| 覆盖平台保留字段名 | 查看平台文档中的保留字列表 |
| Skill 之间硬编码依赖 | 在正文中以自然语言提示"建议先调用 /other-skill" |

---

## 十、安全检查清单

在完成一个 Skill 之前验证：

- [ ] `name` 符合命名规范（小写+连字符，≤64字符）
- [ ] `description` 具体、简洁、第三人称、≤1024字符
- [ ] 触发条件清晰，Agent 能准确判断何时使用
- [ ] 工作流程可执行，无歧义
- [ ] 错误处理已覆盖常见异常
- [ ] 输出格式已定义
- [ ] 依赖的工具/二进制/配置已声明
- [ ] 无命令注入风险（不把用户输入直接拼入 shell）
- [ ] 已用 `openclaw agent --message "..."` 测试触发准确性
- [ ] 文件已纳入 git 版本管理

---

## 十一、推荐工具和资源

| 资源 | 说明 | 链接 |
|------|------|------|
| **agentskills.io** | 官方标准文档和规范 | <https://agentskills.io> |
| **Anthropic skill-creator** | 官方 Skill 创建辅助 Skill | MCP Market |
| **OpenClaw 文档** | OpenClaw Skill 创建指南 | <https://docs.openclaw.ai/zh-CN/tools/creating-skills> |
| **Claude API 最佳实践** | Anthropic 官方 Skill 编写最佳实践 | <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices> |
| **Anthropic Skills 示例库** | 官方 Skill 示例集合 | <https://github.com/anthropics/skills> |
| **ClawHub** | OpenClaw Skill 共享生态 | ClawHub |

---

> 📝 **参考**：
> - agentskills.io 官方标准（2026年5月版本）
> - OpenClaw 创建技能文档
> - Claude API Agent Skills 最佳实践
> - SegmentFault:《Skills 从 0 到 1 怎么写：AI Agent Skills 完整创建教程（2026）》
> - UX Planet:《7 Rules for Creating an Effective Claude Code Skill》
