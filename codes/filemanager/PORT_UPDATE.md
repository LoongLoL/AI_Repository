# 🔄 部署配置更新说明

## 📝 更新内容

### 1. 端口号更新
- **旧配置**: 80（HTTP）、443（HTTPS）
- **新配置**: **7890**（HTTP）、7891（HTTPS）

### 2. 部署路径确认
- **确定路径**: `/root/.openclaw/workspace/projects/ai_repo/documents`
- **文件目录**: 同上（不是单独的 `/root/filemanager_data`）

### 3. 旧容器清理
- **新增脚本**: `cleanup-port-7890.sh`
- **作用**: 自动清理服务器上占用 7890 端口的旧 Docker 项目

---

## 🚀 更新后的部署流程

### 第 1 步：清理旧容器（新增）

```bash
# 清理占用 7890 端口的旧 Docker 项目
bash cleanup-port-7890.sh

# 这个脚本会：
# 1. 查找占用 7890 端口的进程
# 2. 查找相关的 Docker 容器
# 3. 停止并删除这些容器
# 4. 验证端口已释放
```

### 第 2 步：上传项目文件

```bash
# 远程部署脚本会自动完成：
bash remote-deploy.sh

# 脚本内容：
# 1. SSH 连接到 192.168.31.246
# 2. 上传项目文件
# 3. 构建 Docker 镜像
# 4. 启动容器（使用 7890 端口）
# 5. 验证服务健康
```

### 第 3 步：访问应用

```
http://192.168.31.246:7890  ← 注意：使用 7890 端口
```

---

## 📊 更新的文件列表

### 已修改的文件

| 文件 | 修改内容 |
|------|---------|
| `docker-compose.yml` | 端口改为 7890→80、7891→443 |
| `docker-compose.yml` | 文件卷改为 `/root/.openclaw/workspace/projects/ai_repo/documents` |
| `remote-deploy.sh` | 添加 DEPLOY_PORT=7890 变量 |
| `START_HERE.md` | 更新访问地址和清理步骤 |

### 新增的文件

| 文件 | 用途 |
|------|------|
| `cleanup-port-7890.sh` | 清理占用 7890 端口的旧容器（Linux/Mac） |
| `cleanup-port-7890.bat` | 清理占用 7890 端口的旧容器（Windows） |
| `PORT_UPDATE.md` | 本文件，更新说明 |

---

## 🔍 关键配置检查

### docker-compose.yml 配置

```yaml
services:
  filemanager:
    # ...
    volumes:
      - /root/.openclaw/workspace/projects/ai_repo/documents:/data/files:ro
  
  nginx:
    ports:
      - "7890:80"    # ← 外部 7890 映射到容器内 80
      - "7891:443"   # ← 外部 7891 映射到容器内 443
```

### 访问地址

```
HTTP:  http://192.168.31.246:7890
HTTPS: https://192.168.31.246:7891  (如需要)
```

---

## 🎯 完整部署步骤

```bash
# 1️⃣  准备环境（本地）
cd d:\Bandzip\filemanager
cp .env.example .env
# 编辑 .env，设置 SECRET_KEY 等

# 2️⃣  清理旧容器（可选但推荐）
bash cleanup-port-7890.sh

# 3️⃣  执行远程部署
bash remote-deploy.sh

# 4️⃣  验证部署
# 浏览器访问：http://192.168.31.246:7890

# 5️⃣  查看日志（如需要）
ssh root@192.168.31.246
cd /root/.openclaw/workspace/projects/ai_repo/documents
docker-compose logs -f
```

---

## ⚠️ 清理脚本详解

### 功能说明

`cleanup-port-7890.sh` 自动执行以下步骤：

1. **检测占用端口的进程**
   ```bash
   netstat -tlnp | grep :7890
   ```

2. **查找关联的 Docker 容器**
   ```bash
   docker ps -q | xargs docker inspect | grep 7890
   ```

3. **停止容器**
   ```bash
   docker stop <container_id>
   ```

4. **删除容器**
   ```bash
   docker rm <container_id>
   ```

5. **验证端口释放**
   ```bash
   netstat -tlnp | grep :7890  # 应该无结果
   ```

### 使用方法

**方式 1：直接运行（Linux/Mac）**

```bash
bash cleanup-port-7890.sh
```

**方式 2：远程执行（通过 SSH）**

```bash
ssh root@192.168.31.246 "bash /tmp/cleanup-port-7890.sh"
```

**方式 3：Windows 下远程执行**

```bash
bash cleanup-port-7890.bat
```

---

## 🔧 手动清理方法（如脚本失败）

如果自动清理脚本不工作，可手动执行：

```bash
# SSH 进入服务器
ssh root@192.168.31.246

# 查找占用 7890 端口的容器
docker ps -a

# 停止容器
docker stop <container_name_or_id>

# 删除容器
docker rm <container_name_or_id>

# 验证端口已释放
netstat -tlnp | grep 7890  # 应该无结果或为空
```

---

## ✅ 部署检查清单

部署前：

- [ ] 已清理 7890 端口的旧容器（或确认端口未被占用）
- [ ] .env 文件已配置
- [ ] SSH 连接正常
- [ ] 网络连接正常

部署中：

- [ ] 文件上传完成
- [ ] 镜像构建成功
- [ ] 容器启动成功

部署后：

- [ ] 可以访问 http://192.168.31.246:7890
- [ ] 文件浏览功能正常
- [ ] 日志无错误

---

## 📞 常见问题

### Q1：7890 端口仍被占用？

```bash
# 强制查找占用的进程
lsof -i :7890

# 强制杀死进程（谨慎！）
kill -9 <PID>

# 或重启 Docker
systemctl restart docker
```

### Q2：Docker 容器无法启动？

```bash
# 查看详细错误日志
docker-compose logs

# 检查端口是否确实释放
netstat -tlnp | grep 7890
```

### Q3：如何还原到 80 端口？

编辑 `docker-compose.yml`：

```yaml
ports:
  - "80:80"      # 改回 80
  - "443:443"    # 改回 443
```

---

## 🎊 下一步

1. **执行清理**
   ```bash
   bash cleanup-port-7890.sh
   ```

2. **执行部署**
   ```bash
   bash remote-deploy.sh
   ```

3. **访问应用**
   ```
   http://192.168.31.246:7890
   ```

---

**更新完成！现在可以使用 7890 端口部署了。** 🚀

---

*更新时间*: 2026-05-25 17:05  
*更新内容*: 端口号从 80 改为 7890，文件路径确认为 `/root/.openclaw/workspace/projects/ai_repo/documents`  
*新增功能*: 旧容器清理脚本 `cleanup-port-7890.sh`
