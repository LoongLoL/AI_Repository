# Docker 快速启动指南

## 前置条件
- ✅ Docker 已安装（版本 20.10+）
- ✅ docker-compose 已安装（版本 1.29+）

---

## 快速启动（5 分钟）

### 第 1 步：准备环境文件

```bash
# 从模板生成 .env 文件
cp .env.example .env

# 编辑 .env，修改以下必要项：
# - SECRET_KEY：生成强密钥（至少50字符）
# - ALLOWED_HOSTS：设置你的域名或 IP
# - FILES_ROOT：确保指向 /data/files
```

**生成强密钥的方法：**

```bash
# 方法 1：使用 Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 方法 2：使用 Python 3
python3 -c "import secrets; print(secrets.token_urlsafe(50))"

# 方法 3：使用 OpenSSL
openssl rand -base64 50
```

### 第 2 步：准备文件目录

```bash
# 创建文件目录（或使用已有的）
mkdir -p /path/to/your/files

# 确保有足够的权限
chmod 755 /path/to/your/files
```

**编辑 docker-compose.yml，修改数据卷路径：**

```yaml
volumes:
  - /path/to/your/files:/data/files:ro  # 改为实际路径
```

### 第 3 步：构建镜像

```bash
# 标准构建（需要 3-5 分钟）
docker build -t filemanager:latest .

# 或使用多阶段构建（镜像更小）
docker build -f Dockerfile.multistage -t filemanager:latest .

# 查看镜像大小
docker images filemanager:latest
```

### 第 4 步：启动服务

```bash
# 后台启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 预期输出：
# NAME                  STATUS
# filemanager_app       Up (healthy)
# filemanager_nginx     Up (healthy)
```

### 第 5 步：验证服务

```bash
# 查看 Django 应用日志
docker-compose logs -f filemanager

# 查看 Nginx 日志
docker-compose logs -f nginx

# 测试应用（应返回 200 OK）
curl http://localhost:8000/

# 访问应用
# 浏览器打开：http://localhost 或 http://your-ip
```

---

## 常用命令

### 查看日志

```bash
# 查看所有日志（最后 100 行）
docker-compose logs --tail=100

# 实时跟踪日志
docker-compose logs -f

# 只看特定服务的日志
docker-compose logs -f filemanager
docker-compose logs -f nginx
```

### 管理容器

```bash
# 停止服务
docker-compose stop

# 重启服务
docker-compose restart

# 完全停止并移除容器
docker-compose down

# 停止并移除所有数据（包括数据卷）
docker-compose down -v

# 进入容器调试
docker exec -it filemanager_app bash

# 查看容器资源使用
docker stats
```

### 查看服务状态

```bash
# 查看容器进程
docker-compose ps

# 检查容器健康状态
docker-compose ps --no-trunc

# 查看网络信息
docker network inspect filemanager_network
```

---

## 常见问题快速解决

### ❌ 容器无法启动

```bash
# 查看错误日志
docker-compose logs filemanager

# 常见原因及解决：
# 1. FILES_ROOT 路径不存在
#    → 检查 docker-compose.yml 中的 volumes 配置
# 2. SECRET_KEY 未设置
#    → 检查 .env 文件中的 SECRET_KEY
# 3. 权限不足
#    → 运行：chmod 755 /path/to/your/files
```

### ❌ 无法访问文件

```bash
# 检查文件挂载
docker exec filemanager_app ls -la /data/files

# 检查容器权限
docker exec filemanager_app whoami

# 如果目录为空，说明宿主机路径不正确
# 修改 docker-compose.yml 中的 volumes 部分
```

### ❌ Nginx 502 错误

```bash
# 检查 Django 应用是否运行
docker-compose ps

# 查看 Django 应用日志
docker-compose logs filemanager

# 重启 Nginx
docker-compose restart nginx
```

### ❌ 大文件下载超时

```bash
# 编辑 nginx.conf，检查以下设置：
proxy_connect_timeout 60s;
proxy_send_timeout 300s;
proxy_read_timeout 300s;
client_max_body_size 100M;

# 然后重启 Nginx
docker-compose restart nginx
```

### ⚠️ 内存不足

```bash
# 查看内存使用
docker stats

# 在 docker-compose.yml 中调整资源限制
deploy:
  resources:
    limits:
      memory: 2G
    reservations:
      memory: 512M
```

---

## 生产环境部署清单

必须检查：

- [ ] `.env` 文件已创建且未提交到 git
- [ ] `DEBUG=False` 已设置
- [ ] `SECRET_KEY` 是强密钥（50+ 字符）
- [ ] `ALLOWED_HOSTS` 设置正确
- [ ] 文件目录路径正确且权限充足
- [ ] Nginx SSL 证书已准备（如需 HTTPS）
- [ ] 数据卷已配置为只读（`:ro`）
- [ ] 资源限制已设置
- [ ] 日志收集已配置
- [ ] 健康检查可正常工作
- [ ] 已测试大文件下载

---

## 性能优化建议

### 1. 调整工作进程数

```yaml
# docker-compose.yml
environment:
  - WORKERS=8  # CPU核心数 * 2 + 1

# 或编辑 Dockerfile CMD 中的 --workers 参数
```

### 2. 启用 Gzip 压缩

已在 `nginx.conf` 中配置，自动启用。

### 3. 设置静态文件缓存

已在 `nginx.conf` 中配置，30天缓存。

### 4. 监控容器性能

```bash
# 实时监控
docker stats --no-stream=false

# 查看内存泄漏（持续监控）
watch -n 1 'docker stats --no-stream'
```

---

## 升级和更新

### 更新应用代码

```bash
# 1. 停止服务
docker-compose down

# 2. 拉取最新代码
git pull origin main

# 3. 重新构建镜像
docker build -t filemanager:latest .

# 4. 启动服务
docker-compose up -d
```

### 更新依赖

```bash
# 1. 更新 requirements.txt
# 2. 重新构建镜像
docker build --no-cache -t filemanager:latest .

# 3. 重启容器
docker-compose up -d
```

---

## 备份和恢复

### 备份文件

```bash
# 备份文件目录
tar -czf filemanager_backup_$(date +%Y%m%d).tar.gz /path/to/your/files

# 备份数据卷
docker run --rm -v filemanager_logs:/data -v $(pwd):/backup \
  alpine tar czf /backup/logs_backup.tar.gz -C /data .
```

### 恢复文件

```bash
# 从备份恢复
tar -xzf filemanager_backup_20240101.tar.gz -C /path/to/
```

---

## 监控和告警

### 设置监控脚本

```bash
#!/bin/bash
# monitor.sh - 容器监控脚本

while true; do
    STATUS=$(docker-compose ps --services --filter "status=running")
    if [ -z "$STATUS" ]; then
        echo "警告：服务已停止"
        # 可添加告警逻辑（如发送邮件）
    fi
    sleep 60
done
```

### 运行监控

```bash
chmod +x monitor.sh
./monitor.sh &
```

---

## 清理和维护

### 清理无用的镜像和容器

```bash
# 清理停止的容器
docker container prune -f

# 清理无用的镜像
docker image prune -f

# 清理无用的卷
docker volume prune -f

# 完全清理（谨慎！）
docker system prune -a --volumes
```

### 查看磁盘使用

```bash
# 查看 Docker 磁盘使用
docker system df

# 详细信息
docker system df -v
```

---

## 获取帮助

### 查看容器日志

```bash
docker-compose logs [SERVICE_NAME]
```

### 进入容器交互式 Shell

```bash
docker exec -it filemanager_app bash
```

### 测试网络连接

```bash
docker exec filemanager_app curl -v http://filemanager:8000/
```

---

**需要帮助？参考 DOCKER_DEPLOYMENT.md 获取更详细的说明。**
