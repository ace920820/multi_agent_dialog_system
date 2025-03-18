@echo off
rem 医疗助手系统 - API测试脚本 (Windows批处理版本)

echo ===================================================
echo 医疗助手系统 - 聊天API测试 (批处理版本)
echo ===================================================

set /p user_id=请输入用户ID (默认为test_user): 

if "%user_id%"=="" (
    set user_id=test_user
)

echo.
echo 用户ID已设置为: %user_id%
echo 您可以开始与系统对话了。输入'exit'结束测试。
echo ---------------------------------------------------

:chat_loop
echo.
set /p message=请输入您的消息: 

if "%message%"=="exit" goto :eof

echo 正在发送请求...
echo.

rem 使用curl发送POST请求
curl -X POST http://127.0.0.1:5000/api/chat ^
     -H "Content-Type: application/json" ^
     -d "{\"user_id\":\"%user_id%\", \"message\":\"%message%\"}" ^
     -s

echo.
echo ---------------------------------------------------

goto chat_loop
