#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
医疗助手系统 - API测试脚本

用于测试系统的聊天API接口
"""

import requests
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("医疗助手系统测试脚本")

# API地址
API_URL = "http://127.0.0.1:5000/api/chat"

def send_message(user_id, message):
    """
    向聊天API发送消息并获取响应
    
    Args:
        user_id: 用户ID
        message: 用户消息内容
        
    Returns:
        API响应结果
    """
    # 构建请求数据
    payload = {
        "user_id": user_id,
        "message": message
    }
    
    # 打印发送的请求
    logger.info(f"发送请求到 {API_URL}")
    logger.info(f"请求数据: {json.dumps(payload, ensure_ascii=False)}")
    
    try:
        # 发送POST请求
        response = requests.post(API_URL, json=payload)
        
        # 检查响应状态
        if response.status_code == 200:
            # 解析JSON响应
            result = response.json()
            logger.info(f"收到成功响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return result
        else:
            logger.error(f"请求失败，状态码: {response.status_code}")
            logger.error(f"错误响应: {response.text}")
            return {"error": f"请求失败，状态码: {response.status_code}"}
            
    except Exception as e:
        logger.error(f"发送请求时出错: {str(e)}")
        return {"error": str(e)}

def interactive_test():
    """交互式测试聊天API"""
    print("=" * 50)
    print("医疗助手系统 - 聊天API测试")
    print("=" * 50)
    
    # 获取用户ID
    user_id = input("请输入用户ID (默认为'test_user'): ").strip() or "test_user"
    
    print(f"\n用户ID已设置为: {user_id}")
    print("您可以开始与系统对话了。输入'退出'或'exit'结束测试。")
    print("-" * 50)
    
    while True:
        # 获取用户消息
        user_message = input("\n请输入您的消息: ").strip()
        
        # 检查是否退出
        if user_message.lower() in ["退出", "exit", "quit", "q"]:
            print("测试已结束。")
            break
            
        # 发送消息并获取响应
        response = send_message(user_id, user_message)
        
        # 显示响应
        if "response" in response:
            print("\n系统响应:")
            print(response["response"])
        elif "error" in response:
            print(f"\n错误: {response['error']}")
        else:
            print(f"\n收到未知格式的响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
            
        print("-" * 50)

if __name__ == "__main__":
    interactive_test()
