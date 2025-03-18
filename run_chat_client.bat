@echo off
:: 医疗助手系统 - 聊天客户端启动脚本
:: 该脚本用于启动Python聊天客户端测试工具

echo ==============================================
echo 医疗助手系统 - 聊天客户端启动脚本
echo ==============================================

:: 设置Python路径
set PYTHON_PATH=D:\Users\cupid\anaconda3\envs\py39_env\python.exe

:: 检查Python路径是否存在
if not exist "%PYTHON_PATH%" (
    echo 错误: 无法找到Python解释器!
    echo 配置的路径: %PYTHON_PATH%
    echo 请检查Python安装路径并更新此脚本中的PYTHON_PATH变量
    pause
    exit /b 1
)

:: 显示准备启动信息
echo 正在使用 %PYTHON_PATH% 启动聊天客户端...
echo.

:: 启动Python脚本
"%PYTHON_PATH%" chat_client.py

:: 脚本执行完毕
echo.
echo 聊天客户端已关闭
pause
