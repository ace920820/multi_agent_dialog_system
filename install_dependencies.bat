@echo off
:: 安装项目依赖的批处理脚本

echo ================================================
echo 医疗助手系统 - 安装依赖
echo ================================================

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

:: 显示准备安装信息
echo 正在使用 %PYTHON_PATH% 安装依赖...
echo.

:: 安装依赖
echo 安装 Flask-CORS...
"%PYTHON_PATH%" -m pip install flask-cors

echo.
echo 依赖安装完成
pause
