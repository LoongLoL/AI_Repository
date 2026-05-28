#!/bin/bash
# remote-deploy.sh - 远程服务器一键部署脚本
# 使用方法：
#   1. 编辑此文件中的 SERVER_IP、SERVER_USER、PROJECT_PATH
#   2. 运行：./remote-deploy.sh
#   或者：bash remote-deploy.sh

set -e

# ========== 配置信息 ==========
SERVER_IP="192.168.31.246"
SERVER_USER="root"
SERVER_PORT="22"
PROJECT_PATH="/root/.openclaw/workspace/projects/ai_repo/documents"
LOCAL_PROJECT_PATH="."
DEPLOY_PORT=7890

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "==================================================="
echo "Django 文件管理器 远程部署脚本"
echo "==================================================="
echo ""
echo -e "${BLUE}部署配置:${NC}"
echo "  服务器地址: $SERVER_IP"
echo "  服务器用户: $SERVER_USER"
echo "  项目路径: $PROJECT_PATH"
echo "  部署端口: $DEPLOY_PORT"
echo ""

# 检查 SSH 连接
echo -e "${YELLOW}[1/7]${NC} 检查 SSH 连接..."
if ! ssh -o ConnectTimeout=5 -p $SERVER_PORT $SERVER_USER@$SERVER_IP "echo OK" &> /dev/null; then
    echo -e "${RED}✗ 无法连接到服务器 $SERVER_IP${NC}"
    echo "请检查:"
    echo "  1. 服务器地址是否正确"
    echo "  2. SSH 是否可用"
    echo "  3. 网络连接是否正常"
    exit 1
fi
echo -e "${GREEN}✓ SSH 连接成功${NC}"

# 在服务器上创建项目目录
echo -e "${YELLOW}[2/7]${NC} 在服务器上创建项目目录..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "mkdir -p $PROJECT_PATH"
echo -e "${GREEN}✓ 目录创建完成${NC}"

# 上传项目文件
echo -e "${YELLOW}[3/7]${NC} 上传项目文件到服务器..."
rsync -avz --delete \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='*.log' \
    --exclude='db.sqlite3' \
    --exclude='staticfiles' \
    --exclude='node_modules' \
    -e "ssh -p $SERVER_PORT" \
    "$LOCAL_PROJECT_PATH/" "$SERVER_USER@$SERVER_IP:$PROJECT_PATH/"
echo -e "${GREEN}✓ 项目文件上传完成${NC}"

# 上传 .env 文件（如果存在）
echo -e "${YELLOW}[4/7]${NC} 上传环境配置文件..."
if [ -f ".env" ]; then
    scp -P $SERVER_PORT .env $SERVER_USER@$SERVER_IP:$PROJECT_PATH/.env
    echo -e "${GREEN}✓ .env 文件上传完成${NC}"
else
    echo -e "${YELLOW}⚠ .env 文件未找到，请手动上传或在服务器上创建${NC}"
fi

# 在服务器上修改文件权限
echo -e "${YELLOW}[5/7]${NC} 设置服务器上的文件权限..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "chmod +x $PROJECT_PATH/deploy.sh"
echo -e "${GREEN}✓ 权限设置完成${NC}"

# 在服务器上构建 Docker 镜像
echo -e "${YELLOW}[6/7]${NC} 在服务器上构建 Docker 镜像..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "cd $PROJECT_PATH && docker build -t filemanager:latest ."
echo -e "${GREEN}✓ 镜像构建完成${NC}"

# 在服务器上启动容器
echo -e "${YELLOW}[7/7]${NC} 在服务器上启动服务..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "cd $PROJECT_PATH && docker-compose up -d"
echo -e "${GREEN}✓ 服务启动完成${NC}"

echo ""
echo "==================================================="
echo -e "${GREEN}远程部署完成！${NC}"
echo "==================================================="
echo ""
echo -e "${BLUE}访问应用:${NC}"
echo "  HTTP:  http://$SERVER_IP"
echo ""
echo -e "${BLUE}查看服务状态:${NC}"
echo "  ssh $SERVER_USER@$SERVER_IP"
echo "  cd $PROJECT_PATH"
echo "  docker-compose ps"
echo ""
echo -e "${BLUE}查看日志:${NC}"
echo "  ssh $SERVER_USER@$SERVER_IP"
echo "  cd $PROJECT_PATH"
echo "  docker-compose logs -f filemanager"
echo ""
echo -e "${BLUE}停止服务:${NC}"
echo "  ssh $SERVER_USER@$SERVER_IP"
echo "  cd $PROJECT_PATH"
echo "  docker-compose down"
echo ""
