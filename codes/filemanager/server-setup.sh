#!/bin/bash
# server-setup.sh - 在服务器上执行的部署脚本
# 用途：服务器环境配置和容器启动
# 使用方法：
#   1. 上传此文件到服务器
#   2. 运行：bash server-setup.sh

set -e

PROJECT_PATH="/root/.openclaw/workspace/projects/ai_repo/documents"
FILES_PATH="/root/filemanager_data"

echo "==================================================="
echo "Django 文件管理器 - 服务器端部署"
echo "==================================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 第 1 步：检查 Docker
echo -e "${YELLOW}[1/6]${NC} 检查 Docker 环境..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker 未安装${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ docker-compose 未安装${NC}"
    exit 1
fi

DOCKER_VERSION=$(docker --version | awk '{print $3}' | cut -d',' -f1)
echo -e "${GREEN}✓ Docker 版本: $DOCKER_VERSION${NC}"

# 第 2 步：创建项目目录
echo -e "${YELLOW}[2/6]${NC} 设置项目目录..."
if [ ! -d "$PROJECT_PATH" ]; then
    mkdir -p "$PROJECT_PATH"
    echo -e "${GREEN}✓ 创建项目目录: $PROJECT_PATH${NC}"
else
    echo -e "${GREEN}✓ 项目目录已存在${NC}"
fi

# 第 3 步：创建文件数据卷
echo -e "${YELLOW}[3/6]${NC} 设置文件数据卷..."
if [ ! -d "$FILES_PATH" ]; then
    mkdir -p "$FILES_PATH"
    chmod 755 "$FILES_PATH"
    echo -e "${GREEN}✓ 创建文件目录: $FILES_PATH${NC}"
else
    echo -e "${GREEN}✓ 文件目录已存在${NC}"
fi

# 第 4 步：验证必要文件
echo -e "${YELLOW}[4/6]${NC} 检查必要文件..."
REQUIRED_FILES=(
    "docker-compose.yml"
    "Dockerfile"
    "nginx.conf"
    ".env"
    "requirements.txt"
)

cd "$PROJECT_PATH"

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ 缺少文件: $file${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✓ 所有必要文件已就位${NC}"

# 第 5 步：构建 Docker 镜像
echo -e "${YELLOW}[5/6]${NC} 构建 Docker 镜像..."
if docker build -t filemanager:latest .; then
    echo -e "${GREEN}✓ Docker 镜像构建成功${NC}"
    DOCKER_IMAGE_SIZE=$(docker images filemanager:latest --format "{{.Size}}")
    echo "  镜像大小: $DOCKER_IMAGE_SIZE"
else
    echo -e "${RED}✗ Docker 镜像构建失败${NC}"
    exit 1
fi

# 第 6 步：启动容器
echo -e "${YELLOW}[6/6]${NC} 启动服务容器..."

# 检查端口是否可用
for port in 80 443 8000; do
    if netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        echo -e "${YELLOW}⚠ 端口 $port 已被占用${NC}"
    fi
done

if docker-compose up -d; then
    echo -e "${GREEN}✓ 容器启动成功${NC}"
else
    echo -e "${RED}✗ 容器启动失败${NC}"
    docker-compose logs
    exit 1
fi

# 等待服务就绪
echo ""
echo "等待服务就绪（最多 40 秒）..."
for i in {1..40}; do
    if curl -f http://localhost:8000/ &> /dev/null; then
        echo -e "${GREEN}✓ 服务已就绪${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# 显示最终信息
echo ""
echo "==================================================="
echo -e "${GREEN}部署完成！${NC}"
echo "==================================================="
echo ""
echo -e "${BLUE}访问应用:${NC}"
echo "  HTTP:  http://$(hostname -I | awk '{print $1}')"
echo ""
echo -e "${BLUE}查看服务状态:${NC}"
echo "  docker-compose ps"
echo ""
echo -e "${BLUE}查看日志:${NC}"
echo "  docker-compose logs -f filemanager"
echo ""
echo -e "${BLUE}停止服务:${NC}"
echo "  docker-compose down"
echo ""
echo -e "${BLUE}项目路径:${NC}"
echo "  $PROJECT_PATH"
echo ""
echo -e "${BLUE}文件数据:${NC}"
echo "  $FILES_PATH"
echo ""
