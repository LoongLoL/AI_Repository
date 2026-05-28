#!/bin/bash
# deploy-with-cleanup.sh - 一键部署（包含清理功能）
# 使用方法：bash deploy-with-cleanup.sh

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║           Django 文件管理器 - 一键部署（包含清理功能）           ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

SERVER="192.168.31.246"
USER="root"
PROJECT_PATH="/root/.openclaw/workspace/projects/ai_repo/documents"
DEPLOY_PORT=7890

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 第 1 步：清理旧容器
echo -e "${YELLOW}[1/3] 清理占用 $DEPLOY_PORT 端口的旧容器...${NC}"
echo ""

# 上传清理脚本
echo "上传清理脚本到服务器..."
scp -P 22 cleanup-port-7890.sh $USER@$SERVER:/tmp/ 2>/dev/null || true

# 执行清理脚本
echo "执行清理操作..."
ssh -p 22 $USER@$SERVER "bash /tmp/cleanup-port-7890.sh 2>/dev/null || true"

sleep 2

echo -e "${GREEN}✓ 清理完成${NC}"
echo ""

# 第 2 步：执行部署
echo -e "${YELLOW}[2/3] 执行部署...${NC}"
echo ""

bash remote-deploy.sh

echo ""
echo -e "${GREEN}✓ 部署完成${NC}"
echo ""

# 第 3 步：显示访问信息
echo -e "${YELLOW}[3/3] 验证部署...${NC}"
echo ""

sleep 3

echo -e "${BLUE}部署信息:${NC}"
echo "  服务器地址: $SERVER"
echo "  部署端口: $DEPLOY_PORT"
echo "  应用访问: http://$SERVER:$DEPLOY_PORT"
echo ""

echo "尝试连接应用..."
if curl -f http://$SERVER:$DEPLOY_PORT/ &> /dev/null; then
    echo -e "${GREEN}✓ 应用已就绪！${NC}"
else
    echo -e "${YELLOW}⚠ 应用未就绪，请稍候几秒后刷新浏览器${NC}"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo -e "║  ${GREEN}🎉 部署完成！${NC}                                               ║"
echo -e "║  访问地址: http://$SERVER:$DEPLOY_PORT                  ║"
echo "║                                                                    ║"
echo "║  查看日志:                                                         ║"
echo "║    ssh $USER@$SERVER                                     ║"
echo "║    cd $PROJECT_PATH                ║"
echo "║    docker-compose logs -f filemanager                             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
