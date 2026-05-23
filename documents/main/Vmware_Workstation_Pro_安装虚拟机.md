# VMware Workstation Pro 安装虚拟机完整指南

> 系统：Debian 13.x 64-bit XFCE | 适用开发环境搭建

---

## 一、虚拟机系统

**系统选择：Debian 13.x 64-bit XFCE**

XFCE 桌面系统的优势：相比 GNOME，XFCE 内存消耗更低，适合在虚拟机中流畅运行。

---

## 二、系统设置

### 硬件配置

| 项目 | 配置 |
|------|------|
| 内存 | 8 GB |
| CPU | 2 核 4 线程 |
| 硬盘 | 60 GB（单文件） |
| 网络 | 桥接模式，使用宿主机实体网卡 |
| 显卡 | 启用 Accelerate 3D Graphics，显存 2 GB |

**CPU 重要提示：** 勾选「Virtualize Intel VT-x/EPT or AMD-V/RVI」可提升虚拟化性能，但需宿主机关闭以下功能：

- Hyper-V
- WSL2
- Windows 沙盒
- 虚拟机监控程序平台
- 虚拟机平台
- 内存完整性验证
- Win11 需额外注意基于虚拟化的安全性(VBS)是否禁用

### 共享文件夹

在 Options 中配置共享文件夹，方便宿主机与虚拟机之间传输文件。

### 系统安装选项

安装时只选择以下三项：

- SSH server
- XFCE desktop
- standard system utilities

---

## 三、系统优化

### 1. 安装 VMware Tools

```bash
sudo apt update
sudo apt install open-vm-tools open-vm-tools-desktop -y
```

### 2. 设置 APT 更新源（清华大学镜像）

编辑 `/etc/apt/sources.list`，替换为国内源：

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ trixie main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ trixie-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security trixie-security main contrib non-free non-free-firmware
```

更新软件包：

```bash
sudo apt update
sudo apt upgrade -y
```

### 3. 设置 Swap

Swap 建议大小：

| 物理内存 | 推荐 Swap |
|---------|----------|
| 8 GB | 8 GB |
| 16 GB | 12 GB |

配置命令：

```bash
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
# 永久启用
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 4. 安装必要工具

```bash
sudo apt install curl git htop neofetch build-essential -y
```

### 5. 配置 SSH 登录（密钥登录更安全）

**设置 root 密码：**

```bash
sudo passwd root
```

**编辑 SSH 配置** `/etc/ssh/sshd_config`：

```ini
PermitRootLogin yes               # 允许 root 登录
# PermitRootLogin prohibit-password  # 仅密钥登录（更安全）
PasswordAuthentication yes        # 允许密码登录
PubkeyAuthentication yes          # 开启 SSH key 登录
```

**在 Windows 上生成密钥对：**

```bash
ssh-keygen -t rsa -b 4096
```

密钥文件默认位置：

```
# 私钥
C:\Users\你的用户名\.ssh\id_rsa
# 公钥
C:\Users\你的用户名\.ssh\id_rsa.pub
```

**上传公钥到虚拟机：**

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
# 将公钥内容粘贴进去
nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**Windows 使用私钥登录：**

```bash
ssh -i ~/.ssh/id_rsa root@192.168.x.x -p 22
```

---

## 四、安装软件

### 1. Docker

**设置 Docker APT 仓库：**

```bash
# 添加 Docker GPG key
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 添加仓库源
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: bookworm
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```

> **注意：** 若使用 Debian 测试版(trixie)，需将 `$(. /etc/os-release && echo "$VERSION_CODENAME")` 替换为 `trixie`。

**安装 Docker：**

```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**配置国内镜像加速：**

编辑 `/etc/docker/daemon.json`：

```json
{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.xuanyuan.me",
    "https://hub.rat.dev",
    "https://docker.m.daocloud.io",
    "https://docker.unsee.tech"
  ],
  "max-concurrent-downloads": 10,
  "max-download-attempts": 5
}
```

重启并测试：

```bash
systemctl daemon-reload
systemctl restart docker
sudo docker run hello-world
```

### 2. OpenClaw

OpenClaw 是一款开源的 AI 助手框架，支持本地部署。

**安装方式一：使用安装脚本（推荐）**

```bash
curl -fsSL https://get.openclaw.ai | bash
```

**安装方式二：使用 npm 全局安装**

```bash
# 前提：已安装 Node.js 18+
npm install -g openclaw
```

**安装方式三：Docker 部署**

```bash
docker pull openclaw/gateway:latest
docker run -d \
  --name openclaw-gateway \
  -p 19000:19000 \
  -v openclaw_data:/root/.openclaw \
  openclaw/gateway:latest
```

**初始化配置：**

```bash
openclaw configure
```

按照提示配置 API Key、聊天频道等信息。

### 3. MySQL

**使用 apt 安装：**

```bash
sudo apt install mariadb-server -y    # Debian 默认提供 MariaDB
```

如需安装官方 MySQL 8：

```bash
# 下载 MySQL APT 配置包
wget https://repo.mysql.com/mysql-apt-config_0.8.33-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.33-1_all.deb
sudo apt update
sudo apt install mysql-server -y
```

**或使用 Docker 部署：**

```bash
docker run -d \
  --name mysql8 \
  -e MYSQL_ROOT_PASSWORD=your_secure_password \
  -e MYSQL_DATABASE=devdb \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  mysql:8
```

**安全配置：**

```bash
sudo mysql_secure_installation
```

### 4. SQL Server（Docker 部署）

Microsoft SQL Server 在 Linux 上官方推荐通过 Docker 部署。

```bash
docker run -d \
  --name sqlserver \
  -e "ACCEPT_EULA=Y" \
  -e "MSSQL_SA_PASSWORD=YourStrong!Passw0rd" \
  -p 1433:1433 \
  -v sqlserver_data:/var/opt/mssql \
  mcr.microsoft.com/mssql/server:2022-latest
```

**常用管理命令：**

```bash
# 进入容器
docker exec -it sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U SA -P "YourStrong!Passw0rd" -C

# 创建数据库
CREATE DATABASE DemoDB;
GO

# 查看数据库列表
SELECT name FROM sys.databases;
GO
```

> **注意：** 宿主机需至少 2 GB 可用内存，生产环境建议 4 GB+。

### 5. Redis

**使用 apt 安装：**

```bash
sudo apt install redis-server -y
```

**配置 Redis：**

编辑 `/etc/redis/redis.conf`：

```ini
# 绑定地址（开发环境可注释掉仅限本机）
bind 127.0.0.1 ::1

# 设置密码（建议生产环境设置）
requirepass your_redis_password

# 持久化
save 900 1
save 300 10
save 60 10000
```

**管理 Redis 服务：**

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server
```

**测试连接：**

```bash
redis-cli ping
# 输出: PONG
```

**或使用 Docker 部署：**

```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  -v redis_data:/data \
  redis:7-alpine \
  redis-server --appendonly yes --requirepass your_redis_password
```

### 6. Nginx

**安装：**

```bash
sudo apt install nginx -y
```

**管理 Nginx：**

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

**验证安装：**

访问 `http://<虚拟机IP>`，应看到 Nginx 欢迎页面。

**基础配置示例：**

创建站点配置文件 `/etc/nginx/sites-available/dev-site`：

```nginx
server {
    listen 80;
    server_name dev.local;

    root /var/www/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/dev-site /etc/nginx/sites-enabled/
sudo nginx -t          # 测试配置
sudo systemctl reload nginx  # 重载配置
```

---

## 五、总结

至此，你的 Debian 13 + XFCE 虚拟机已具备完整的开发环境：

| 服务 | 用途 | 端口 |
|------|------|------|
| Docker | 容器化部署 | - |
| OpenClaw | AI 助手框架 | 19000 |
| MySQL/MariaDB | 关系数据库 | 3306 |
| SQL Server | 企业级数据库 | 1433 |
| Redis | 缓存/队列 | 6379 |
| Nginx | Web 服务器/反向代理 | 80/443 |

> **最后建议：** 创建虚拟机快照，方便后续出问题时快速回滚。
