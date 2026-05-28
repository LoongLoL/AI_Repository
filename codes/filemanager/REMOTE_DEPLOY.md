# 远程服务器部署指南

## 📍 目标服务器信息

- **服务器 IP**: 192.168.31.246
- **服务器用户**: root
- **部署路径**: /root/.openclaw/workspace/projects/ai_repo/documents
- **容器配置**: Docker + Nginx + Gunicorn

---

## 🚀 快速部署（推荐）

### 方法 1：使用一键部署脚本（最简单）

**前提**: 你的本地机器已安装 SSH 和 rsync

```bash
# 1. 编辑脚本中的配置（如需要）
nano remote-deploy.sh

# 2. 运行部署脚本
bash remote-deploy.sh

# 或添加执行权限后直接运行
chmod +x remote-deploy.sh
./remote-deploy.sh
```

**脚本会自动执行以下步骤**:
1. ✅ 检查 SSH 连接
2. ✅ 创建远程项目目录
3. ✅ 上传项目文件
4. ✅ 上传 .env 配置
5. ✅ 设置文件权限
6. ✅ 构建 Docker 镜像
7. ✅ 启动容器

---

## 🔧 手动部署步骤

如果一键部署脚本失败，可按以下步骤手动操作：

### 第 1 步：SSH 连接到服务器

```bash
ssh root@192.168.31.246
```

### 第 2 步：创建项目目录

```bash
mkdir -p /root/.openclaw/workspace/projects/ai_repo/documents
cd /root/.openclaw/workspace/projects/ai_repo/documents
```

### 第 3 步：上传项目文件

在本地机器上执行：

```bash
# 使用 scp 上传单个文件
scp -r /path/to/filemanager root@192.168.31.246:/root/.openclaw/workspace/projects/ai_repo/documents/

# 或使用 rsync（更高效，支持增量同步）
rsync -avz --delete \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='.env' \
  --exclude='*.log' \
  /path/to/filemanager/ root@192.168.31.246:/root/.openclaw/workspace/projects/ai_repo/documents/
```

### 第 4 步：在服务器上创建 .env 文件

```bash
# 在服务器上
cd /root/.openclaw/workspace/projects/ai_repo/documents

# 从模板生成 .env
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here-minimum-50-characters
ALLOWED_HOSTS=192.168.31.246,localhost,127.0.0.1
FILES_ROOT=/data/files
EOF
```

### 第 5 步：准备文件数据卷

```bash
# 在服务器上创建文件目录（或使用已有的目录）
mkdir -p /root/filemanager_data

# 如果有源文件，复制到该目录
cp -r /path/to/your/files/* /root/filemanager_data/

# 设置权限
chmod 755 /root/filemanager_data
chmod 644 /root/filemanager_data/*
```

### 第 6 步：编辑 docker-compose.yml

```bash
# 在服务器上编辑配置
vi /root/.openclaw/workspace/projects/ai_repo/documents/docker-compose.yml

# 修改 volumes 部分：
# 把这一行：
#   - /path/to/your/files:/data/files:ro
# 改为：
#   - /root/filemanager_data:/data/files:ro
```

### 第 7 步：构建 Docker 镜像

```bash
cd /root/.openclaw/workspace/projects/ai_repo/documents

# 构建镜像（这需要 3-5 分钟）
docker build -t filemanager:latest .

# 或使用多阶段构建（镜像更小）
docker build -f Dockerfile.multistage -t filemanager:latest .

# 查看镜像大小
docker images filemanager:latest
```

### 第 8 步：启动容器

```bash
cd /root/.openclaw/workspace/projects/ai_repo/documents

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 预期输出：
# NAME                  STATUS
# filemanager_app       Up (healthy)
# filemanager_nginx     Up (healthy)
```

### 第 9 步：验证应用

```bash
# 查看 Django 应用日志
docker-compose logs -f filemanager

# 在另一个终端测试应用
curl http://localhost:8000/

# 或在浏览器访问
# http://192.168.31.246
```

---

## 📋 验证检查清单

部署完成后，验证以下项目：

- [ ] SSH 连接正常
- [ ] 项目文件已上传
- [ ] .env 文件已配置
- [ ] Docker 镜像已构建
- [ ] 容器状态为 "Up"
- [ ] 健康检查通过 (healthy)
- [ ] 可以访问应用 (http://192.168.31.246)
- [ ] 文件目录可访问
- [ ] Nginx 反向代理工作正常
- [ ] 日志无异常错误

---

## 🔍 常见问题排查

### 问题 1：SSH 连接失败

```bash
# 检查网络连接
ping 192.168.31.246

# 检查 SSH 服务是否运行
ssh -v root@192.168.31.246

# 如果提示权限拒绝，检查公钥是否配置
```

### 问题 2：上传文件超慢

```bash
# 使用 rsync 而不是 scp（支持断点续传）
rsync -avz --partial --progress \
  /path/to/filemanager/ root@192.168.31.246:/root/.openclaw/workspace/projects/ai_repo/documents/
```

### 问题 3：Docker 镜像构建失败

```bash
# 查看错误日志
docker build -t filemanager:latest . --progress=plain

# 检查 Dockerfile 语法
docker run --rm -i hadolint/hadolint < Dockerfile

# 检查依赖包
cat requirements.txt
```

### 问题 4：容器无法启动

```bash
# 查看容器日志
docker-compose logs filemanager

# 查看容器详细信息
docker inspect filemanager_app

# 检查端口是否被占用
netstat -tlnp | grep 8000

# 如被占用，修改 docker-compose.yml 中的端口
```

### 问题 5：无法访问应用

```bash
# 检查容器是否运行
docker-compose ps

# 检查 Nginx 是否运行
docker-compose ps | grep nginx

# 查看 Nginx 错误日志
docker-compose logs nginx

# 测试应用连接
docker-compose exec filemanager curl http://localhost:8000/

# 检查防火墙规则
sudo firewall-cmd --list-all
# 或
sudo ufw status
```

### 问题 6：文件目录权限问题

```bash
# 检查目录权限
ls -la /root/filemanager_data

# 调整权限
chmod 755 /root/filemanager_data
chmod 644 /root/filemanager_data/*

# 检查容器内的权限
docker-compose exec filemanager ls -la /data/files
```

---

## 🛠️ 维护和管理

### 查看日志

```bash
# 实时查看所有日志
docker-compose logs -f

# 查看特定服务的日志
docker-compose logs -f filemanager
docker-compose logs -f nginx

# 查看最后 100 行日志
docker-compose logs --tail=100

# 导出日志到文件
docker-compose logs > logs_backup.txt
```

### 更新应用

```bash
cd /root/.openclaw/workspace/projects/ai_repo/documents

# 拉取最新代码（如使用 git）
git pull origin main

# 或从本地上传最新文件
rsync -avz --delete /path/to/filemanager/ root@192.168.31.246:/root/.openclaw/workspace/projects/ai_repo/documents/

# 重新构建镜像
docker build -t filemanager:latest .

# 重启容器
docker-compose restart
```

### 停止和启动服务

```bash
# 停止所有容器
docker-compose stop

# 启动容器
docker-compose start

# 重启容器
docker-compose restart

# 完全停止并移除容器
docker-compose down

# 停止并移除所有数据卷
docker-compose down -v
```

### 监控容器性能

```bash
# 实时监控
docker stats

# 查看容器内存使用
docker stats --no-stream

# 查看容器进程
docker top filemanager_app
```

---

## 💾 备份和恢复

### 备份文件

```bash
# 备份整个项目目录
tar -czf filemanager_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  /root/.openclaw/workspace/projects/ai_repo/documents/

# 备份数据卷
docker run --rm -v /root/filemanager_data:/data -v /tmp:/backup \
  alpine tar czf /backup/files_backup_$(date +%Y%m%d).tar.gz -C /data .

# 下载备份到本地
scp root@192.168.31.246:/tmp/files_backup_*.tar.gz ./
```

### 恢复备份

```bash
# 恢复项目目录
tar -xzf filemanager_backup_20240101_120000.tar.gz -C /

# 恢复文件数据
docker run --rm -v /root/filemanager_data:/data -v /tmp:/backup \
  alpine tar xzf /backup/files_backup_20240101.tar.gz -C /data
```

---

## 🔐 安全建议

### 1. 生产环境配置

```bash
# 确保 DEBUG=False
grep DEBUG /root/.openclaw/workspace/projects/ai_repo/documents/.env

# 确保 SECRET_KEY 是强密钥
grep SECRET_KEY /root/.openclaw/workspace/projects/ai_repo/documents/.env
```

### 2. 防火墙规则

```bash
# 只允许指定 IP 访问（可选）
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.31.0/24" port protocol="tcp" port="80" accept' --permanent

# 或使用 ufw
sudo ufw allow from 192.168.31.0/24 to any port 80
```

### 3. SSL/HTTPS 配置

```bash
# 生成自签名证书
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout /root/filemanager_data/server.key \
  -out /root/filemanager_data/server.crt \
  -days 365

# 编辑 nginx.conf 启用 HTTPS
# 取消相关注释并重启
docker-compose restart nginx
```

---

## 📊 性能监控

### 设置监控脚本

```bash
# 创建监控脚本
cat > /root/monitor_filemanager.sh << 'EOF'
#!/bin/bash
while true; do
    clear
    echo "=== Django 文件管理器 监控 ==="
    echo "时间: $(date)"
    echo ""
    echo "容器状态:"
    docker-compose -f /root/.openclaw/workspace/projects/ai_repo/documents/docker-compose.yml ps
    echo ""
    echo "资源使用:"
    docker stats --no-stream
    sleep 5
done
EOF

chmod +x /root/monitor_filemanager.sh

# 运行监控
/root/monitor_filemanager.sh
```

---

## 📞 故障排除

如遇到问题，请按以下顺序排查：

1. **网络连接**
   ```bash
   ping 192.168.31.246
   ssh root@192.168.31.246 "echo OK"
   ```

2. **Docker 服务**
   ```bash
   ssh root@192.168.31.246 "docker ps"
   ssh root@192.168.31.246 "docker-compose ps"
   ```

3. **应用日志**
   ```bash
   ssh root@192.168.31.246 "cd /root/.openclaw/workspace/projects/ai_repo/documents && docker-compose logs"
   ```

4. **系统资源**
   ```bash
   ssh root@192.168.31.246 "df -h && free -h"
   ```

---

## 🎯 下一步

部署完成后，建议：

1. ✅ 测试文件上传/下载功能
2. ✅ 验证大文件处理性能
3. ✅ 配置日志收集和监控
4. ✅ 设置自动备份策略
5. ✅ 配置 SSL/HTTPS 证书
6. ✅ 实施访问控制和认证

---

**文档更新时间**: 2026 年 5 月 25 日

如有问题，请参考 DOCKER_DEPLOYMENT.md 获取更详细的信息。
