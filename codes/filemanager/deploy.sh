#!/bin/bash
# deploy.sh - 一键部署脚本
# 使用方法：./deploy.sh 或 bash deploy.sh

set -e

echo "==================================================="
echo "Django 文件管理器 Docker 部署脚本"
echo "==================================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Docker 安装
echo -e "${YELLOW}[1/5]${NC} 检查 Docker 安装状态..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker 已安装${NC}"

# 检查 docker-compose 安装
echo -e "${YELLOW}[2/5]${NC} 检查 docker-compose 安装状态..."
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ docker-compose 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✓ docker-compose 已安装${NC}"

# 检查 .env 文件
echo -e "${YELLOW}[3/5]${NC} 检查环境配置文件..."
if [ ! -f .env ]; then
    echo -e "${RED}✗ .env 文件不存在${NC}"
    echo "请先运行: cp .env.example .env 并编辑配置"
    exit 1
fi
echo -e "${GREEN}✓ .env 文件已存在${NC}"

# 构建镜像
echo -e "${YELLOW}[4/5]${NC} 构建 Docker 镜像..."
docker build -t filemanager:latest .
echo -e "${GREEN}✓ 镜像构建完成${NC}"

# 启动容器
echo -e "${YELLOW}[5/5]${NC} 启动服务..."
docker-compose up -d
echo -e "${GREEN}✓ 服务启动完成${NC}"

# 等待服务就绪
echo ""
echo "等待服务就绪（最多 40 秒）..."
for i in {1..40}; do
    if curl -f http://localhost:8000/ &> /dev/null; then
        echo -e "${GREEN}✓ 服务就绪${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

echo ""
echo "==================================================="
echo -e "${GREEN}部署完成！${NC}"
echo "==================================================="
echo ""
echo "访问应用:"
echo "  HTTP:  http://localhost"
echo ""
echo "查看日志:"
echo "  docker-compose logs -f filemanager"
echo ""
echo "停止服务:"
echo "  docker-compose down"
echo ""
