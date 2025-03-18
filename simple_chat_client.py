#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
医疗助手系统 - 简易聊天API测试客户端
"""

import requests
import json

# API地址
API_URL = "http://127.0.0.1:5000/api/chat"

def main():
    """主函数 - 简单的聊天API测试"""
    print("=" * 50)
    print("医疗助手系统 - 简易聊天API测试客户端")
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
            
        # 构建请求数据
        payload = {
            "user_id": user_id,
            "message": user_message
        }
        
        print("正在发送请求，请稍候...")
        
        try:
            # 发送POST请求
            response = requests.post(API_URL, json=payload)
            
            # 检查响应状态
            if response.status_code == 200:
                # 解析JSON响应
                result = response.json()
                print("\n系统响应:")
                if "response" in result:
                    print(result["response"])
                else:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"\n请求失败，状态码: {response.status_code}")
                print(f"错误响应: {response.text}")
                
        except Exception as e:
            print(f"\n发送请求时出错: {str(e)}")
            
        print("-" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已被用户终止。")
    except Exception as e:
        print(f"\n程序运行时出现错误: {str(e)}")
