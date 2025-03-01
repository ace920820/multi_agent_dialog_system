#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
多智能体驱动的智能医疗助手系统 - 主入口

提供Flask API接口服务，集成所有智能体功能
"""

from flask import Flask, request, jsonify
import json
import logging
from datetime import datetime
import os

# 导入智能体组件
from agentlite.agents import BaseAgent
from agents.manager_agent import MedicalManagerAgent
from agents.appointment_agent import AppointmentAgent
from agents.guide_agent import GuideAgent
from agents.consultation_agent import ConsultationAgent

# 导入数据模型
from models.user import UserModel
from models.doctor import DoctorModel
from models.department import DepartmentModel
from models.appointment import AppointmentModel

# 导入API管理器
from api.api_manager import ApiManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("医疗助手系统")

# 初始化Flask应用
app = Flask(__name__)

# 全局变量
manager_agent = None
api_manager = None
user_model = None
doctor_model = None
department_model = None
appointment_model = None

# 会话存储
sessions = {}


def init_system():
    """初始化系统组件"""
    global manager_agent, api_manager, user_model, doctor_model, department_model, appointment_model
    
    logger.info("正在初始化系统组件...")
    
    try:
        # 初始化API管理器
        api_manager = ApiManager()
        logger.info("API管理器初始化完成")
        
        # 初始化数据模型
        user_model = UserModel()
        logger.info("用户模型初始化完成")
        
        doctor_model = DoctorModel()
        logger.info("医生模型初始化完成")
        
        department_model = DepartmentModel()
        logger.info("科室模型初始化完成")
        
        appointment_model = AppointmentModel()
        logger.info("预约模型初始化完成")
        
        # 创建预约挂号智能体
        appointment_agent = AppointmentAgent(
            name="预约挂号智能体",
            role="负责收集用户信息、分析症状、推荐科室和医生，并管理预约",
            actions=[]
        )
        logger.info("预约挂号智能体初始化完成")
        
        # 创建导诊推荐智能体
        guide_agent = GuideAgent(
            name="导诊推荐智能体",
            role="负责症状采集、分析和科室匹配",
            actions=[]
        )
        logger.info("导诊推荐智能体初始化完成")
        
        # 创建医疗咨询智能体
        consultation_agent = ConsultationAgent(
            name="医疗咨询智能体",
            role="提供健康问题解答、就医建议、用药指导和检查解读",
            actions=[]
        )
        logger.info("医疗咨询智能体初始化完成")
        
        # 创建管理智能体
        team = [appointment_agent, guide_agent, consultation_agent]
        manager_agent = MedicalManagerAgent(
            name="管理智能体",
            role="管理整个服务流程，分解任务并分配给个体智能体",
            team_agents=team
        )
        logger.info("管理智能体初始化完成")
        
        logger.info("所有系统组件初始化完成")
        
    except Exception as e:
        logger.error(f"系统初始化失败: {str(e)}", exc_info=True)
        raise


@app.route('/api/health', methods=['GET'])
def health_check():
    """系统健康检查接口"""
    logger.info("接收到健康检查请求")
    
    status = "ok" if all([
        manager_agent is not None,
        api_manager is not None,
        user_model is not None,
        doctor_model is not None,
        department_model is not None,
        appointment_model is not None
    ]) else "error"
    
    response = {
        "status": status,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "components": {
            "manager_agent": manager_agent is not None,
            "api_manager": api_manager is not None,
            "models": {
                "user": user_model is not None,
                "doctor": doctor_model is not None,
                "department": department_model is not None,
                "appointment": appointment_model is not None
            }
        }
    }
    
    logger.info(f"健康检查结果: {status}")
    return jsonify(response)


@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天接口，处理用户消息并返回系统响应"""
    try:
        # 解析请求数据
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
        
        # 获取或创建会话
        if user_id not in sessions:
            logger.info(f"为用户[{user_id}]创建新会话")
            sessions[user_id] = {
                "history": [],
                "user_info": {},
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        # 记录用户消息
        sessions[user_id]["history"].append({
            "role": "user", 
            "content": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # 创建任务包
        task_package = {
            "instruction": message,
            "completion": "Incomplete",
            "creator": "System",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "answer": "",
            "executor": "ManagerAgent",
            "user_id": user_id,
            "session": sessions[user_id]
        }
        
        logger.info(f"创建任务包: user_id={user_id}, instruction={message[:30]}...")
        
        # 管理智能体处理任务
        logger.info("管理智能体开始处理任务")
        prompt = manager_agent.generate_prompt(task_package)
        logger.debug(f"生成的提示词: {prompt[:100]}...")
        
        action = manager_agent.llm(prompt)
        logger.debug(f"LLM生成的动作: {str(action)[:100]}...")
        
        result = manager_agent.run_action(action)
        logger.info(f"任务执行结果: {result[:100]}...")
        
        # 更新任务包
        task_package["answer"] = result
        task_package["completion"] = "Completed"
        
        # 记录系统响应
        sessions[user_id]["history"].append({
            "role": "system", 
            "content": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # 检查会话历史长度，防止内存占用过多
        if len(sessions[user_id]["history"]) > 50:
            logger.info(f"会话历史过长，进行截断: user_id={user_id}")
            sessions[user_id]["history"] = sessions[user_id]["history"][-30:]
        
        response_data = {
            "response": result,
            "user_id": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        logger.info(f"响应用户[{user_id}]成功")
        return jsonify(response_data)
    
    except Exception as e:
        logger.error(f"处理聊天请求时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user_info(user_id):
    """获取用户信息接口"""
    try:
        logger.info(f"收到获取用户信息请求: user_id={user_id}")
        
        if not user_model:
            logger.error("用户模型未初始化")
            return jsonify({"error": "用户模型未初始化"}), 500
        
        user_info = user_model.get_user_info(user_id)
        if not user_info:
            logger.warning(f"用户不存在: user_id={user_id}")
            return jsonify({"error": "用户不存在"}), 404
        
        logger.info(f"成功获取用户信息: user_id={user_id}")
        return jsonify(user_info)
    
    except Exception as e:
        logger.error(f"获取用户信息时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/departments', methods=['GET'])
def get_departments():
    """获取科室列表接口"""
    try:
        logger.info("收到获取科室列表请求")
        
        if not department_model:
            logger.error("科室模型未初始化")
            return jsonify({"error": "科室模型未初始化"}), 500
        
        departments = department_model.get_all_departments()
        logger.info(f"成功获取科室列表，共 {len(departments)} 个科室")
        return jsonify(departments)
    
    except Exception as e:
        logger.error(f"获取科室列表时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """获取医生列表接口"""
    try:
        department_id = request.args.get('department_id')
        if department_id:
            logger.info(f"收到获取特定科室医生列表请求: department_id={department_id}")
        else:
            logger.info("收到获取所有医生列表请求")
        
        if not doctor_model:
            logger.error("医生模型未初始化")
            return jsonify({"error": "医生模型未初始化"}), 500
        
        if department_id:
            doctors = doctor_model.get_doctors_by_department(department_id)
            logger.info(f"成功获取科室[{department_id}]的医生列表，共 {len(doctors)} 名医生")
        else:
            doctors = doctor_model.get_all_doctors()
            logger.info(f"成功获取所有医生列表，共 {len(doctors)} 名医生")
        
        return jsonify(doctors)
    
    except Exception as e:
        logger.error(f"获取医生列表时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/appointments', methods=['POST'])
def create_appointment():
    """创建预约接口"""
    try:
        logger.info("收到创建预约请求")
        
        if not appointment_model:
            logger.error("预约模型未初始化")
            return jsonify({"error": "预约模型未初始化"}), 500
        
        data = request.json
        if not data:
            logger.warning("收到无效的预约请求数据")
            return jsonify({"error": "无效的请求数据"}), 400
        
        required_fields = ['user_id', 'doctor_id', 'appointment_time']
        for field in required_fields:
            if field not in data:
                logger.warning(f"预约请求缺少必要字段: {field}")
                return jsonify({"error": f"缺少必要字段: {field}"}), 400
        
        logger.info(f"预约信息: user_id={data['user_id']}, doctor_id={data['doctor_id']}, time={data['appointment_time']}")
        
        appointment_id = appointment_model.create_appointment(
            user_id=data['user_id'],
            doctor_id=data['doctor_id'],
            appointment_time=data['appointment_time'],
            remarks=data.get('remarks', '')
        )
        
        logger.info(f"预约创建成功: appointment_id={appointment_id}")
        
        return jsonify({
            "appointment_id": appointment_id,
            "status": "已创建",
            "message": "预约创建成功"
        })
    
    except Exception as e:
        logger.error(f"创建预约时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/appointments/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """获取预约详情接口"""
    try:
        logger.info(f"收到获取预约详情请求: appointment_id={appointment_id}")
        
        if not appointment_model:
            logger.error("预约模型未初始化")
            return jsonify({"error": "预约模型未初始化"}), 500
        
        appointment = appointment_model.get_appointment(appointment_id)
        if not appointment:
            logger.warning(f"预约不存在: appointment_id={appointment_id}")
            return jsonify({"error": "预约不存在"}), 404
        
        logger.info(f"成功获取预约详情: appointment_id={appointment_id}")
        return jsonify(appointment)
    
    except Exception as e:
        logger.error(f"获取预约详情时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/reset_session/<user_id>', methods=['POST'])
def reset_session(user_id):
    """重置用户会话接口"""
    try:
        logger.info(f"收到重置会话请求: user_id={user_id}")
        
        if user_id in sessions:
            del sessions[user_id]
            logger.info(f"已重置用户[{user_id}]的会话")
        else:
            logger.info(f"用户[{user_id}]没有活跃会话，无需重置")
        
        return jsonify({
            "status": "success",
            "message": f"用户[{user_id}]的会话已重置"
        })
    
    except Exception as e:
        logger.error(f"重置会话时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """获取症状列表接口"""
    try:
        logger.info("收到获取症状列表请求")
        
        if not department_model:
            logger.error("科室模型未初始化")
            return jsonify({"error": "科室模型未初始化"}), 500
        
        # 从科室模型中获取所有症状关键词
        all_symptoms = department_model.get_all_symptom_keywords()
        
        logger.info(f"成功获取症状列表，共 {len(all_symptoms)} 个症状")
        return jsonify(all_symptoms)
    
    except Exception as e:
        logger.error(f"获取症状列表时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


@app.route('/api/departments/match', methods=['POST'])
def match_department():
    """根据症状匹配科室接口"""
    try:
        logger.info("收到症状匹配科室请求")
        
        data = request.json
        if not data:
            logger.warning("收到无效的匹配请求数据")
            return jsonify({"error": "无效的请求数据"}), 400
        
        symptoms = data.get("symptoms")
        if not symptoms or not isinstance(symptoms, list):
            logger.warning("症状匹配请求缺少必要的症状列表或格式错误")
            return jsonify({"error": "请提供症状列表"}), 400
        
        logger.info(f"匹配症状: {symptoms}")
        
        if not department_model:
            logger.error("科室模型未初始化")
            return jsonify({"error": "科室模型未初始化"}), 500
        
        matched_departments = department_model.match_departments_by_symptoms(symptoms)
        
        logger.info(f"成功匹配科室，共 {len(matched_departments)} 个匹配结果")
        return jsonify(matched_departments)
    
    except Exception as e:
        logger.error(f"匹配科室时出错: {str(e)}", exc_info=True)
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500


if __name__ == '__main__':
    # 初始化系统
    init_system()
    
    # 获取端口配置，默认为5000
    port = int(os.environ.get('PORT', 5000))
    
    # 启动Flask应用
    logger.info(f"系统启动，监听端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)