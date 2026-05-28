@echo off
REM cleanup-port-7890.bat - Windows 版本清理脚本
REM 使用此脚本通过 SSH 远程清理占用 7890 端口的容器

setlocal enabledelayedexpansion

set SERVER=192.168.31.246
set USER=root

echo ==================================================
echo 远程清理占用 7890 端口的 Docker 容器
echo ==================================================
echo.

echo 连接到服务器: %SERVER%
echo.

REM 上传并执行清理脚本
echo 上传清理脚本...
pscp -P 22 cleanup-port-7890.sh %USER%@%SERVER%:/tmp/cleanup-port-7890.sh

if %errorlevel% neq 0 (
    echo ✗ 上传脚本失败
    pause
    exit /b 1
)

echo.
echo 执行清理脚本...
plink -P 22 %USER%@%SERVER% "bash /tmp/cleanup-port-7890.sh"

if %errorlevel% neq 0 (
    echo ✗ 执行脚本失败
    pause
    exit /b 1
)

echo.
echo ==================================================
echo ✓ 清理完成！
echo ==================================================
pause
