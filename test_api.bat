@echo off
:: 医疗助手系统 - API测试脚本
:: 使用curl命令测试系统的聊天API

echo ================================================
echo 医疗助手系统 - API测试脚本
echo ================================================

:: 设置测试数据
set API_URL=http://127.0.0.1:5000/api/chat
set USER_ID=test_user
set MESSAGE=你好，我想预约看医生

:: 显示将要发送的数据
echo 将向以下API发送请求: %API_URL%
echo 用户ID: %USER_ID%
echo 消息内容: %MESSAGE%
echo.
echo 正在发送请求...

:: 使用curl发送请求
curl -X POST %API_URL% ^
     -H "Content-Type: application/json" ^
     -d "{\"user_id\":\"%USER_ID%\", \"message\":\"%MESSAGE%\"}"

echo.
echo.
echo 请求已完成
echo 使用以下命令可以自定义测试:
echo curl -X POST %API_URL% -H "Content-Type: application/json" -d "{\"user_id\":\"用户ID\", \"message\":\"消息内容\"}"
echo.
pause
