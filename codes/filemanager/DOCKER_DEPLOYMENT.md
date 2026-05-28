# Django 文件管理器 - Docker 发布部署指南

## 目录

1. [快速开始](#快速开始)
2. [Dockerfile 详解](#dockerfile-详解)
3. [docker-compose 部署](#docker-compose-部署)
4. [多阶段构建（优化镜像大小）](#多阶段构建优化镜像大小)
5. [生产部署建议](#生产部署建议)
6. [常见问题](#常见问题)

---

## 快速开始

### 前置条件
- Docker 安装完毕（建议版本 20.10+）
- docker-compose 安装完毕（建议版本 1.29+）

### 方式1：使用 docker-compose（推荐）

1. **复制以下配置文件到项目目录**

```yaml
# docker-compose.yml
version: '3.8'

services:
  filemanager:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FILES_ROOT=/data/files
      - DEBUG=False
      - SECRET_KEY=your-secret-key-here-change-this-in-production
      - ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
    volumes:
      - /path/to/your/files:/data/files:ro
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - filemanager
    restart: unless-stopped
```

2. **启动服务**

```bash
docker-compose up -d
```

3. **查看日志**

```bash
docker-compose logs -f filemanager
```

4. **停止服务**

```bash
docker-compose down
```

---

## Dockerfile 详解

### 基础版本（简单部署）

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（仅需要的）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建静态文件目录
RUN mkdir -p /app/staticfiles /app/logs

# 非 root 用户运行（安全性）
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "filemanager.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

### 多阶段构建版本（优化镜像大小）

```dockerfile
# Dockerfile.multistage
FROM python:3.11-slim as builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 创建虚拟环境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 复制依赖文件
COPY requirements.txt .

# 安装依赖到虚拟环境
RUN pip install --no-cache-dir -r requirements.txt

# ===================== 运行阶段 =====================

FROM python:3.11-slim

WORKDIR /app

# 从 builder 阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 复制应用代码
COPY . .

# 创建必要目录和非 root 用户
RUN mkdir -p /app/staticfiles /app/logs && \
    useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

ENV PATH="/opt/venv/bin:$PATH"
USER appuser

EXPOSE 8000

CMD ["gunicorn", "filemanager.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-tmp-dir", "/dev/shm", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

---

## docker-compose 部署

### 完整示例配置

#### 1. requirements.txt（更新）

```
Django>=4.2,<6.0
gunicorn>=21.0
python-dotenv>=1.0.0
```

#### 2. .env 环境文件

```bash
# .env 文件（不要提交到 git）
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
FILES_ROOT=/data/files
DATABASE_URL=sqlite:///db.sqlite3
WORKERS=4
LOG_LEVEL=info
```

#### 3. nginx 反向代理配置

```nginx
# nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;

    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types text/plain text/css text/xml application/json application/javascript;

    upstream filemanager {
        server filemanager:8000;
    }

    server {
        listen 80;
        server_name _;
        
        client_max_body_size 100M;

        # 静态文件缓存
        location /static/ {
            alias /app/staticfiles/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        # 主应用反向代理
        location / {
            proxy_pass http://filemanager;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # 大文件上传/下载超时
            proxy_connect_timeout 60s;
            proxy_send_timeout 300s;
            proxy_read_timeout 300s;

            # 缓冲设置
            proxy_buffering on;
            proxy_buffer_size 4k;
            proxy_buffers 8 4k;
            proxy_busy_buffers_size 8k;
        }

        # 健康检查端点（可选）
        location /health/ {
            access_log off;
            proxy_pass http://filemanager;
        }
    }
}
```

#### 4. 完整的 docker-compose.yml

```yaml
version: '3.8'

services:
  filemanager:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: filemanager_app
    restart: unless-stopped
    
    environment:
      - DEBUG=${DEBUG:-False}
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - FILES_ROOT=/data/files
    
    volumes:
      # 只读挂载文件根目录
      - /path/to/your/files:/data/files:ro
      # 日志目录
      - filemanager_logs:/app/logs
      # 数据库（如果需要）
      - filemanager_data:/app/db
    
    ports:
      - "8000:8000"
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    networks:
      - filemanager_network
    
    expose:
      - "8000"

  nginx:
    image: nginx:alpine
    container_name: filemanager_nginx
    restart: unless-stopped
    
    ports:
      - "80:80"
      - "443:443"
    
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
      - nginx_logs:/var/log/nginx
    
    depends_on:
      filemanager:
        condition: service_healthy
    
    networks:
      - filemanager_network

volumes:
  filemanager_logs:
    driver: local
  filemanager_data:
    driver: local
  nginx_logs:
    driver: local

networks:
  filemanager_network:
    driver: bridge
```

---

## 多阶段构建优化镜像大小

### 镜像大小对比

| 版本 | 大小 | 优化方式 |
|------|------|---------|
| 基础版本 | ~950MB | Python 3.11-slim |
| 多阶段构建 | ~620MB | 去除构建依赖 |

### 构建命令

```bash
# 标准构建
docker build -t filemanager:latest .

# 使用多阶段 Dockerfile
docker build -f Dockerfile.multistage -t filemanager:latest .

# 带版本标签
docker build -t filemanager:v1.0 -t filemanager:latest .

# 不使用缓存构建
docker build --no-cache -t filemanager:latest .
```

---

## 生产部署建议

### 1. 安全性加固

```dockerfile
# Dockerfile 安全加固版本
FROM python:3.11-slim

WORKDIR /app

# 系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 虚拟环境
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod -R 700 /app/logs

USER appuser

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["gunicorn", "filemanager.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-tmp-dir", "/dev/shm", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

### 2. 环境变量配置模板

```bash
# production.env
DEBUG=False
SECRET_KEY=django-insecure-your-production-secret-key-minimum-50-chars
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
FILES_ROOT=/data/files
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=change-this-password
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

### 3. 日志收集

```yaml
# docker-compose.yml 添加日志配置
services:
  filemanager:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "app=filemanager"
```

### 4. 资源限制

```yaml
services:
  filemanager:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
```

### 5. 监控和健康检查

```yaml
services:
  filemanager:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
  nginx:
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## 常见问题

### Q1: 如何指定 FILES_ROOT？

**方式A - 环境变量**
```bash
docker run -e FILES_ROOT=/data/files -v /path/to/files:/data/files:ro filemanager:latest
```

**方式B - docker-compose**
```yaml
environment:
  - FILES_ROOT=/data/files
volumes:
  - /path/to/files:/data/files:ro
```

---

### Q2: 如何处理大文件上传/下载超时？

在 nginx 配置中增加超时设置：

```nginx
proxy_connect_timeout 60s;
proxy_send_timeout 300s;
proxy_read_timeout 300s;
client_max_body_size 1G;
```

---

### Q3: 如何启用 HTTPS/SSL？

1. **准备证书**
```bash
# 自签名证书（开发用）
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout /path/to/certs/server.key \
  -out /path/to/certs/server.crt \
  -days 365
```

2. **更新 nginx 配置**
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/certs/server.crt;
    ssl_certificate_key /etc/nginx/certs/server.key;
    
    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # ... 其他配置 ...
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

### Q4: 如何扩展到多个工作进程？

```yaml
environment:
  - WORKERS=8

# 或在启动命令中
CMD ["gunicorn", "filemanager.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "8", \
     "--worker-class", "gevent"]
```

---

### Q5: 容器中文件路径权限问题？

```dockerfile
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app /data/files && \
    chmod -R 755 /app && \
    chmod -R 750 /data/files
```

---

### Q6: 如何查看实时日志？

```bash
# 查看 filemanager 容器日志
docker-compose logs -f filemanager

# 查看 nginx 日志
docker-compose logs -f nginx

# 查看最后 100 行日志
docker-compose logs --tail=100 filemanager
```

---

### Q7: 生产环境中应该禁用调试模式吗？

**必须**！在生产环境中：

```bash
# .env
DEBUG=False
```

使用 `DEBUG=False` 时，你需要：
1. 配置正确的 `ALLOWED_HOSTS`
2. 收集静态文件：`python manage.py collectstatic --noinput`
3. 使用生产级 WSGI 服务器（gunicorn）

---

### Q8: 如何处理文件权限问题？

在宿主机上为文件夹设置读权限：

```bash
chmod 755 /path/to/your/files
chmod 644 /path/to/your/files/*
```

然后在 docker-compose 中使用只读挂载：

```yaml
volumes:
  - /path/to/your/files:/data/files:ro
```

---

## 部署检查清单

- [ ] 更新 `requirements.txt`（添加 gunicorn）
- [ ] 创建 `.env` 文件并设置生产配置
- [ ] 修改 `DEBUG=False`
- [ ] 生成强 `SECRET_KEY`
- [ ] 配置正确的 `ALLOWED_HOSTS`
- [ ] 准备 SSL 证书（如果需要 HTTPS）
- [ ] 设置 nginx 配置
- [ ] 测试文件挂载权限
- [ ] 配置日志收集
- [ ] 设置资源限制
- [ ] 设置健康检查
- [ ] 验证 nginx 反向代理工作正常
- [ ] 测试大文件下载功能
- [ ] 监控容器内存和 CPU 使用
- [ ] 设置备份策略

---

## 快速启动命令

```bash
# 构建镜像
docker build -t filemanager:latest .

# 使用 docker-compose 启动
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f filemanager

# 停止服务
docker-compose down

# 完全移除包括数据卷
docker-compose down -v
```

---

## 监控命令

```bash
# 查看容器资源使用
docker stats filemanager_app

# 进入容器调试
docker exec -it filemanager_app bash

# 检查容器网络
docker network inspect filemanager_network
```

---

**本文档持续更新，最后更新时间：2026年**
