@echo off
:: 医疗助手系统 - API服务器启动脚本
:: 该脚本用于启动简化版API服务器

echo ================================================
echo 医疗助手系统 - API服务器启动脚本
echo ================================================

:: 设置Python路径 - 使用系统Python路径
echo 正在启动API服务器...
echo.

:: 启动API服务器
python api_server.py

pause
