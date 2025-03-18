@echo off
:: Medical Assistant System - API Test Script
:: Test the chat API using curl command

echo ================================================
echo Medical Assistant System - API Test Script
echo ================================================

:: Set test data
set API_URL=http://127.0.0.1:5000/api/chat
set USER_ID=test_user
set MESSAGE=Hello, I want to make an appointment with a doctor

:: Display data to be sent
echo API URL: %API_URL%
echo User ID: %USER_ID%
echo Message: %MESSAGE%
echo.
echo Sending request...

:: Send request using curl
curl -X POST %API_URL% ^
     -H "Content-Type: application/json" ^
     -d "{\"user_id\":\"%USER_ID%\", \"message\":\"%MESSAGE%\"}"

echo.
echo.
echo Request completed
echo.
pause
