#!/bin/bash
# cleanup-port-7890.sh - 清理占用 7890 端口的旧 Docker 容器
# 使用方法：
#   1. 上传此脚本到服务器
#   2. 运行：bash cleanup-port-7890.sh

set -e

echo "=================================================="
echo "清理占用 7890 端口的 Docker 容器"
echo "=================================================="
echo ""

PORT=7890

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 第 1 步：查找占用端口的进程
echo -e "${YELLOW}[1/4]${NC} 查找占用端口 $PORT 的进程..."

PIDS=$(netstat -tlnp 2>/dev/null | grep ":$PORT " | awk '{print $NF}' | cut -d'/' -f1 | sort -u)

if [ -z "$PIDS" ]; then
    echo -e "${GREEN}✓ 端口 $PORT 未被占用${NC}"
    echo ""
    echo "可以直接部署新项目"
    exit 0
fi

echo -e "${YELLOW}找到占用端口 $PORT 的进程:${NC}"
for pid in $PIDS; do
    PROCESS=$(ps -p $pid -o comm= 2>/dev/null || echo "未知")
    echo "  PID: $pid - $PROCESS"
done
echo ""

# 第 2 步：查找相关的 Docker 容器
echo -e "${YELLOW}[2/4]${NC} 查找相关的 Docker 容器..."

CONTAINER_IDS=$(docker ps -q 2>/dev/null || true)

if [ -z "$CONTAINER_IDS" ]; then
    echo -e "${YELLOW}⚠ 没有运行中的 Docker 容器${NC}"
    echo ""
    exit 0
fi

MATCHING_CONTAINERS=""

for cid in $CONTAINER_IDS; do
    # 检查容器是否使用了 7890 端口
    PORT_CONFIG=$(docker inspect $cid 2>/dev/null | grep -A 5 "7890" || true)
    
    if [ ! -z "$PORT_CONFIG" ]; then
        CONTAINER_NAME=$(docker inspect -f '{{.Name}}' $cid 2>/dev/null | sed 's/^\/*//')
        echo -e "${YELLOW}找到容器:${NC} $CONTAINER_NAME (ID: $cid)"
        MATCHING_CONTAINERS="$MATCHING_CONTAINERS $cid"
    fi
done

echo ""

# 第 3 步：停止并删除容器
if [ ! -z "$MATCHING_CONTAINERS" ]; then
    echo -e "${YELLOW}[3/4]${NC} 停止容器..."
    for cid in $MATCHING_CONTAINERS; do
        CONTAINER_NAME=$(docker inspect -f '{{.Name}}' $cid 2>/dev/null | sed 's/^\/*//')
        echo -e "${BLUE}停止${NC} $CONTAINER_NAME..."
        docker stop $cid || true
        sleep 2
    done
    echo -e "${GREEN}✓ 容器已停止${NC}"
    echo ""
    
    echo -e "${YELLOW}[4/4]${NC} 删除容器..."
    for cid in $MATCHING_CONTAINERS; do
        CONTAINER_NAME=$(docker inspect -f '{{.Name}}' $cid 2>/dev/null | sed 's/^\/*//')
        echo -e "${RED}删除${NC} $CONTAINER_NAME..."
        docker rm $cid || true
    done
    echo -e "${GREEN}✓ 容器已删除${NC}"
    echo ""
else
    echo -e "${YELLOW}⚠ 未找到使用端口 $PORT 的 Docker 容器${NC}"
    echo ""
fi

# 第 5 步：验证端口是否释放
echo "验证端口状态..."
sleep 2

if netstat -tlnp 2>/dev/null | grep -q ":$PORT "; then
    echo -e "${YELLOW}⚠ 端口 $PORT 仍被占用${NC}"
    echo "占用进程:"
    netstat -tlnp 2>/dev/null | grep ":$PORT "
    echo ""
    echo "建议手动停止进程："
    echo "  kill -9 <PID>"
    exit 1
else
    echo -e "${GREEN}✓ 端口 $PORT 已释放${NC}"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}清理完成！可以开始部署新项目${NC}"
echo "=================================================="
echo ""
echo "下一步："
echo "  cd /root/.openclaw/workspace/projects/ai_repo/documents"
echo "  docker-compose up -d"
echo ""
