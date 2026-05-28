@echo off
REM deploy.bat - Windows 部署脚本
REM 使用方法：双击运行或在 PowerShell 中执行

setlocal enabledelayedexpansion

echo ===================================================
echo Django 文件管理器 Docker 部署脚本 (Windows)
echo ===================================================
echo.

REM 检查 Docker 安装
echo [1/5] 检查 Docker 安装状态...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Docker 未安装
    pause
    exit /b 1
)
echo ✓ Docker 已安装
echo.

REM 检查 docker-compose 安装
echo [2/5] 检查 docker-compose 安装状态...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ docker-compose 未安装
    pause
    exit /b 1
)
echo ✓ docker-compose 已安装
echo.

REM 检查 .env 文件
echo [3/5] 检查环境配置文件...
if not exist ".env" (
    echo ✗ .env 文件不存在
    echo 请先运行: copy .env.example .env 并编辑配置
    pause
    exit /b 1
)
echo ✓ .env 文件已存在
echo.

REM 构建镜像
echo [4/5] 构建 Docker 镜像（这需要几分钟）...
docker build -t filemanager:latest .
if %errorlevel% neq 0 (
    echo ✗ 镜像构建失败
    pause
    exit /b 1
)
echo ✓ 镜像构建完成
echo.

REM 启动容器
echo [5/5] 启动服务...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ✗ 服务启动失败
    pause
    exit /b 1
)
echo ✓ 服务启动完成
echo.

REM 等待服务就绪
echo 等待服务就绪（最多 40 秒）...
for /L %%i in (1,1,40) do (
    timeout /t 1 /nobreak >nul
    echo.
)

echo.
echo ===================================================
echo 部署完成！
echo ===================================================
echo.
echo 访问应用:
echo   HTTP:  http://localhost
echo.
echo 查看日志:
echo   docker-compose logs -f filemanager
echo.
echo 停止服务:
echo   docker-compose down
echo.
pause
