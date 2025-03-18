#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
医疗助手系统 - 聊天API测试客户端
"""

import requests
import json
import logging
import sys
import time

# 配置日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("chat_client.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("医疗聊天客户端")

# API地址配置
API_URL = "http://127.0.0.1:5000/api/chat"

def send_message(user_id, message):
    """
    向聊天API发送消息并获取响应
    
    参数:
        user_id (str): 用户ID
        message (str): 用户消息内容
        
    返回:
        dict: API响应结果
    """
    # 构建请求数据
    payload = {
        "user_id": user_id,
        "message": message
    }
    
    # 记录发送的请求信息
    logger.info(f"正在向API发送请求: {API_URL}")
    logger.info(f"请求数据: user_id={user_id}, message={message}")
    
    try:
        # 发送POST请求
        logger.info("开始发送POST请求...")
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        end_time = time.time()
        
        # 记录请求耗时
        logger.info(f"请求耗时: {end_time - start_time:.2f}秒")
        
        # 检查响应状态
        if response.status_code == 200:
            # 解析JSON响应
            result = response.json()
            logger.info("请求成功，收到响应")
            logger.info(f"响应内容: {json.dumps(result, ensure_ascii=False)}")
            return result
        else:
            # 记录错误状态
            logger.error(f"请求失败，状态码: {response.status_code}")
            logger.error(f"错误响应: {response.text}")
            return {"error": f"请求失败，状态码: {response.status_code}"}
            
    except Exception as e:
        # 记录异常情况
        logger.error(f"发送请求时出现异常: {str(e)}")
        return {"error": str(e)}

def main():
    """
    主函数 - 交互式测试聊天API
    """
    logger.info("=" * 50)
    logger.info("医疗助手系统 - 聊天API测试客户端已启动")
    logger.info("=" * 50)
    
    # 打印欢迎信息
    print("=" * 50)
    print("医疗助手系统 - 聊天API测试客户端")
    print("=" * 50)
    
    # 获取用户ID
    user_id = input("请输入用户ID (默认为'test_user'): ").strip() or "test_user"
    logger.info(f"用户ID已设置为: {user_id}")
    
    print(f"\n用户ID已设置为: {user_id}")
    print("您可以开始与系统对话了。输入'退出'或'exit'结束测试。")
    print("-" * 50)
    
    # 开始交互循环
    while True:
        # 获取用户消息
        user_message = input("\n请输入您的消息: ").strip()
        
        # 检查是否退出
        if user_message.lower() in ["退出", "exit", "quit", "q"]:
            logger.info("用户请求退出测试")
            print("测试已结束。")
            break
            
        # 记录用户输入
        logger.info(f"用户输入: {user_message}")
        
        # 发送消息并获取响应
        print("正在发送请求，请稍候...")
        response = send_message(user_id, user_message)
        
        # 显示响应
        if "response" in response:
            print("\n系统响应:")
            print(response["response"])
            logger.info("已向用户显示系统响应")
        elif "error" in response:
            print(f"\n错误: {response['error']}")
            logger.error(f"向用户显示错误: {response['error']}")
        else:
            print(f"\n收到未知格式的响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
            logger.warning(f"收到未知格式的响应: {json.dumps(response, ensure_ascii=False)}")
            
        print("-" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("用户通过Ctrl+C终止了程序")
        print("\n程序已被用户终止。")
    except Exception as e:
        logger.error(f"程序运行时出现异常: {str(e)}")
        print(f"\n程序运行时出现错误: {str(e)}")
