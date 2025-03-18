#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
医疗助手系统 - API服务器
简化版本，用于测试API接口
"""

from flask import Flask, request, jsonify
import logging
import json
from datetime import datetime

# 配置日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api_server.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("医疗API服务器")

# 初始化Flask应用
app = Flask(__name__)

# 允许跨域请求的简单实现
@app.after_request
def after_request(response):
    """
    为所有响应添加CORS头信息，允许跨域请求
    """
    response.headers.add('Access-Control-Allow-Origin', '*')  # 允许任何源
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')  # 允许的请求头
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')  # 允许的HTTP方法
    return response

@app.route('/api/health', methods=['GET'])
def health_check():
    """系统健康检查接口"""
    logger.info("接收到健康检查请求")
    
    response = {
        "status": "ok",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "message": "API服务器运行正常"
    }
    
    logger.info("返回健康检查响应")
    return jsonify(response)

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """
    聊天接口，处理用户消息并返回系统响应
    支持OPTIONS请求，用于预检
    """
    # 处理CORS预检请求
    if request.method == 'OPTIONS':
        logger.info("收到OPTIONS预检请求")
        return '', 200
        
    try:
        # 解析请求数据
        logger.info("收到聊天请求")
        data = request.json
        if not data:
            logger.warning("收到无效的聊天请求数据")
            return jsonify({"error": "无效的请求数据"}), 400
        
        user_id = data.get("user_id")
        message = data.get("message")
        
        if not user_id or not message:
            logger.warning(f"聊天请求缺少必要参数: user_id={user_id}, message={'有内容' if message else '无内容'}")
            return jsonify({"error": "用户ID和消息不能为空"}), 400
        
        logger.info(f"收到用户[{user_id}]的消息: {message}")
        
        # 模拟处理逻辑
        logger.info("处理用户消息...")
        
        # 生成响应（这里只是一个简单的回显测试）
        response = f"您好，用户{user_id}！我已收到您的消息：\"{message}\"。目前系统正在开发中，暂时无法提供完整功能。"
        
        logger.info(f"生成响应: {response[:50]}...")
        
        response_data = {
            "response": response,
            "user_id": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        logger.info(f"响应用户[{user_id}]成功")
        return jsonify(response_data)
    
    except Exception as e:
        logger.error(f"处理聊天请求时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500

if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("医疗助手系统 - API服务器启动")
    logger.info("=" * 50)
    # 启动Flask应用
    app.run(host='0.0.0.0', port=5000, debug=False)
