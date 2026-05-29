# 🔍 系统安全/完整性/健康性检查报告

**检查时间：** 2026-05-30 03:30 (Asia/Shanghai)
**检查范围：** 系统安全、Skills 完整性、定时任务、Openclaw 代码完整性

---

## 1️⃣ 系统安全/完整性/健康性

### 基础信息

| 项目 | 状态 | 详情 |
|------|------|------|
| 操作系统 | ✅ | Debian 13 Trixie, 内核 6.12.90 |
| 运行时间 | ⚠️ 11 分钟 | 刚重启过（Firecrawl 配置变更导致） |
| 内存 | ✅ | 7.7GB 总量，使用 3.2GB，可用 4.6GB |
| 磁盘 | ✅ | 54% (29G/56G) |
| Swap | ✅ | 11GB 未使用 |
| 自动安全更新 | ✅ | unattended-upgrades active |

### 安全风险

| 风险项 | 级别 | 详情 | 建议 |
|--------|------|------|------|
| SSH 密码登录 | 🔴 高 | `PasswordAuthentication yes` | 改为 no，仅用密钥 |
| iptables 全开放 | 🔴 高 | INPUT 链 policy ACCEPT，无入站过滤 | 添加规则仅放行必要端口 |
| Redis 无认证 | 🔴 高 | 端口 6379 对外暴露且无密码 | 设置 requirepass |
| allowInsecureAuth | 🟡 中 | openclaw.json 中 `allowInsecureAuth: true` | 改为 false |
| .env 文件权限 | 🟡 中 | `/root/.openclaw/.env` 权限 644（全局可读，含 API Key） | chmod 600 |
| Docker root 运行 | 🟡 中 | 7/8 容器以 root 运行 | 创建非 root 用户（局域网环境可接受） |

### Docker 容器状态

| 容器 | 状态 | 端口 | 用户 |
|------|------|------|------|
| searxng | ✅ Up | 8080 | root |
| searxng-redis | ✅ Up (healthy) | 6379 | root |
| filemanager_app | ✅ Up (healthy) | 8000 | root |
| filemanager_nginx | ✅ Up (healthy) | 7890/7891 | root |
| redis-cache | ✅ Up | 6379 | root |
| mysql8.0 | ✅ Up | 3380 | root |
| mariadb10.3 | ✅ Up | 3313 | root |
| sqlserver-db | ✅ Up | 1433 | mssql |

### 已修复项

- ✅ Firecrawl 配置已从 openclaw.json 中移除
- ✅ firecrawl_backend Docker 网络已清理
- ✅ 29 个 firecrawl skills 已删除
- ✅ Firecrawl API Key 已从 bash_history 中清除

---

## 2️⃣ Skills 安全性完整性

### 统计

- **总 Skills 数：** 125 个（~/.agents/skills: 119，workspace/skills: 6）
- **安全审查工具：** prompt-guard ✅、skill-safety-scanner ✅、security-check ✅

### 安全扫描结果

| 检查项 | 状态 |
|--------|------|
| 危险模式扫描 | ✅ 全部通过 |
| 告警项 | 5 个均为误报（关键词出现在注释/说明文字中） |
| 被审查 skill | build-perf-baseline、dotnet-maui-doctor、pi-planning-with-files、planning-with-files、security-check |

### Skills 列表

**~/.agents/skills (119 个)：**
add-lang, agent-eval, analyzing-dotnet-performance, android-tombstone-symbolication, assertion-quality, author-component, binlog-failure-analysis, binlog-generation, build-parallelism, build-perf-baseline, build-perf-diagnostics, check-bin-obj-clash, chef-assistant, chinese-novelist, clawprobe, clr-activation-debugging, code-testing-agent, code-testing-extensions, collect-user-input, configure-auth, configuring-opentelemetry-dotnet, convert-blazor-server-to-webapp, convert-to-cpm, coordinate-components, coverage-analysis, crap-score, create-blazor-project, create-custom-agent, create-skill, create-skill-test, csharp-scripts, daily-ai-news, detect-static-dependencies, directory-build-organization, dotnet-aot-compat, dotnet-maui-doctor, dotnet-pinvoke, dotnet-test-frameworks, dotnet-trace-collect, dotnet-webapi, dump-collect, eval-performance, extension-points, fetch-and-send-data, filter-syntax, find-skills, generate-testability-wrappers, git-commit, hackernews, including-generated-files, incremental-build, item-management, maui-app-lifecycle, maui-collectionview, maui-data-binding, maui-dependency-injection, maui-safe-area, maui-shell-navigation, maui-theming, mcp-csharp-create, mcp-csharp-debug, mcp-csharp-publish, mcp-csharp-test, microbenchmarking, migrate-dotnet10-to-dotnet11, migrate-dotnet8-to-dotnet9, migrate-dotnet9-to-dotnet10, migrate-mstest-v1v2-to-v3, migrate-mstest-v3-to-v4, migrate-nullable-references, migrate-static-to-wrapper, migrate-vstest-to-mtp, migrate-xunit-to-xunit-v3, minimal-api-file-upload, msbuild-antipatterns, msbuild-modernization, msbuild-server, mtp-hot-reload, news-summary, nuget-trusted-publishing, optimizing-ef-core-queries, pdf, pi-planning-with-files, planning-with-files, planning-with-files-ar, planning-with-files-de, planning-with-files-es, planning-with-files-zh, planning-with-files-zht, plan-ui-change, platform-detection, pptx, prompt-guard, property-patterns, python-design-patterns, python-performance-optimization, python-testing-patterns, resolve-project-references, run-tests, security-check, skill-finder, skill-safety-scanner, support-prerendering, system-text-json-net11, target-authoring, tavily-search, technology-selection, template-authoring, template-discovery, template-instantiation, template-validation, test-anti-patterns, test-gap-analysis, test-smell-detection, test-tagging, thread-abort-migration, use-js-interop, writing-mstest-tests

**workspace/skills (6 个)：**
answer-marker, bilibili-search, cooking-recipe, multi-search-engine, news-summary, superpowers

---

## 3️⃣ 定时任务完整性

| 任务 ID | 名称 | 频率 | 状态 | 上次运行 |
|---------|------|------|------|----------|
| b87fabdf | 每日新闻采集-v2 | 每天 11:00 | ✅ 正常 | 成功，耗时 ~412s |
| 65cf18c5 | nightly-git-sync | 每天 02:00 | ✅ 正常 | 成功，耗时 ~48s |

---

## 4️⃣ Openclaw 代码完整性

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 版本 | ✅ 2026.5.27 | 正式版 |
| 安装来源 | ✅ 官方 | `curl -fsSL https://openclaw.ai/install.sh \| bash` |
| dist 文件完整性 | ✅ | 294 个 npm 包完整嵌套 |
| 代码篡改 | ✅ 未发现 | 无可疑注入或后门 |
| /btw 命令 | ✅ 内置功能 | openclaw 2026.5.27 原生自带 |
| 依赖版本冲突 | ⚠️ 3处微小差异 | @anthropic-ai/sdk、@aws-sdk、protobufjs（由子包引起，非恶意） |

---

## 5️⃣ 文件服务器状态

- **地址：** `http://192.168.31.246:7890` ✅ 正常
- **已上传文件：** 32 个（main/: 26 个，news/: 6 个）
- **Git 同步：** ✅ 工作区干净，与 remote 一致

---

## 总结

| 维度 | 评分 | 说明 |
|------|------|------|
| 系统安全 | ⚠️ 中等 | 3 个高危项需修复（SSH、iptas、Redis） |
| Skills 安全 | ✅ 良好 | 125 个 skills 全部通过安全扫描 |
| 定时任务 | ✅ 正常 | 2 个任务均正常运行 |
| 代码完整性 | ✅ 正常 | openclaw 未被篡改 |

**优先修复建议：**
1. SSH 关闭密码登录
2. iptables 添加入站规则
3. Redis 设置密码
4. .env 文件权限收紧
