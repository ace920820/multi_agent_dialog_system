"""
预约挂号动作模块 - 定义预约挂号智能体可执行的动作
"""
import logging
from typing import Dict, Any
from agentlite.actions import BaseAction
from api.mock_data_service import get_departments, get_doctors, get_appointment_slots

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CollectUserInfoAction(BaseAction):
    """收集用户基本信息动作"""
    
    action_name = "CollectUserInfo"
    action_desc = "收集用户的基本信息，如姓名、性别、年龄和联系方式"
    params_doc = {
        "name": "用户姓名",
        "gender": "用户性别",
        "age": "用户年龄",
        "contact": "联系方式"
    }
    
    def __call__(self, **kwargs):
        """执行收集用户信息动作"""
        logger.info(f"收集用户基本信息: {kwargs}")
        
        # 验证必要参数
        required_params = ["name", "gender", "age", "contact"]
        for param in required_params:
            if param not in kwargs:
                error_msg = f"缺少必要参数: {param}"
                logger.error(error_msg)
                return f"错误: {error_msg}"
        
        # 执行收集用户信息的逻辑
        collected_info = {
            "name": kwargs.get("name"),
            "gender": kwargs.get("gender"),
            "age": kwargs.get("age"),
            "contact": kwargs.get("contact")
        }
        
        # 返回收集结果
        result = f"已成功收集用户基本信息: 姓名={collected_info['name']}, 性别={collected_info['gender']}, 年龄={collected_info['age']}, 联系方式={collected_info['contact']}"
        logger.info(result)
        return result


class AnalyzeSymptomsAction(BaseAction):
    """分析症状信息动作"""
    
    action_name = "AnalyzeSymptoms"
    action_desc = "分析用户描述的症状信息，为后续科室推荐做准备"
    params_doc = {
        "symptoms": "用户描述的症状",
        "duration": "症状持续时间",
        "severity": "症状严重程度"
    }
    
    def __call__(self, **kwargs):
        """执行分析症状动作"""
        logger.info(f"分析症状信息: {kwargs}")
        
        # 验证必要参数
        if "symptoms" not in kwargs:
            error_msg = "缺少必要参数: symptoms"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        symptoms = kwargs.get("symptoms")
        duration = kwargs.get("duration", "未知")
        severity = kwargs.get("severity", "未知")
        
        # 执行症状分析逻辑
        # 这里是简化的示例，实际应用中可能需要更复杂的逻辑
        symptom_analysis = "根据症状分析，可能与以下科室相关："
        
        # 简单的关键词匹配
        if any(kw in symptoms.lower() for kw in ["头痛", "头晕", "神经"]):
            symptom_analysis += "\n- 神经内科：处理神经系统疾病"
            
        if any(kw in symptoms.lower() for kw in ["胃痛", "腹痛", "消化", "胃"]):
            symptom_analysis += "\n- 消化内科：处理消化系统疾病"
            
        if any(kw in symptoms.lower() for kw in ["咳嗽", "呼吸", "肺"]):
            symptom_analysis += "\n- 呼吸内科：处理呼吸系统疾病"
            
        if any(kw in symptoms.lower() for kw in ["皮肤", "痒", "疹"]):
            symptom_analysis += "\n- 皮肤科：处理皮肤相关疾病"
            
        # 如果没有匹配到任何科室，给出通用建议
        if symptom_analysis == "根据症状分析，可能与以下科室相关：":
            symptom_analysis += "\n- 建议先去内科进行初步诊断"
        
        # 添加持续时间和严重程度的建议
        symptom_analysis += f"\n\n症状持续时间: {duration}"
        symptom_analysis += f"\n症状严重程度: {severity}"
        
        if duration.lower() in ["长", "长时间", "慢性"] or any(kw in duration.lower() for kw in ["周", "月", "年"]):
            symptom_analysis += "\n建议: 考虑到症状持续时间较长，建议尽快就医"
            
        if severity.lower() in ["严重", "剧烈", "难忍"]:
            symptom_analysis += "\n注意: 症状严重，请考虑紧急就医"
        
        # 返回分析结果
        logger.info(f"症状分析完成")
        return symptom_analysis


class RecommendDepartmentAction(BaseAction):
    """推荐科室动作"""
    
    action_name = "RecommendDepartment"
    action_desc = "根据用户症状信息推荐合适的就诊科室"
    params_doc = {
        "symptoms": "用户症状描述",
        "prefer_location": "用户偏好的医院位置（可选）"
    }
    
    def __call__(self, **kwargs):
        """执行推荐科室动作"""
        logger.info(f"推荐科室: {kwargs}")
        
        # 验证必要参数
        if "symptoms" not in kwargs:
            error_msg = "缺少必要参数: symptoms"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        symptoms = kwargs.get("symptoms")
        prefer_location = kwargs.get("prefer_location", None)
        
        # 调用模拟的部门数据服务
        try:
            departments = get_departments(symptoms, prefer_location)
            logger.info(f"获取到 {len(departments)} 个匹配的科室")
        except Exception as e:
            error_msg = f"获取科室数据失败: {str(e)}"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        if not departments:
            no_result = "没有找到匹配的科室，建议先去内科进行初步诊断"
            logger.warning(no_result)
            return no_result
        
        # 格式化推荐结果
        result = "根据您的症状，推荐以下科室：\n\n"
        
        for dept in departments:
            result += f"- {dept['name']}: {dept['description']}\n"
            result += f"  位置: {dept['location']}\n"
            result += f"  专长: {dept['expertise']}\n\n"
            
        logger.info("科室推荐完成")
        return result


class RecommendDoctorAction(BaseAction):
    """推荐医生动作"""
    
    action_name = "RecommendDoctor"
    action_desc = "根据用户需求和科室信息推荐合适的医生"
    params_doc = {
        "department": "科室名称",
        "prefer_gender": "偏好的医生性别（可选）",
        "prefer_seniority": "偏好的医生资历（可选，如：主任医师、副主任医师等）"
    }
    
    def __call__(self, **kwargs):
        """执行推荐医生动作"""
        logger.info(f"推荐医生: {kwargs}")
        
        # 验证必要参数
        if "department" not in kwargs:
            error_msg = "缺少必要参数: department"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        department = kwargs.get("department")
        prefer_gender = kwargs.get("prefer_gender", None)
        prefer_seniority = kwargs.get("prefer_seniority", None)
        
        # 调用模拟的医生数据服务
        try:
            doctors = get_doctors(department, prefer_gender, prefer_seniority)
            logger.info(f"获取到 {len(doctors)} 个匹配的医生")
        except Exception as e:
            error_msg = f"获取医生数据失败: {str(e)}"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        if not doctors:
            no_result = f"没有找到匹配的{department}科医生"
            logger.warning(no_result)
            return no_result
        
        # 格式化推荐结果
        result = f"根据您的需求，推荐以下{department}科医生：\n\n"
        
        for doctor in doctors:
            result += f"- {doctor['name']} ({doctor['gender']}), {doctor['title']}\n"
            result += f"  专长: {doctor['expertise']}\n"
            result += f"  评分: {doctor['rating']}/5.0\n"
            result += f"  出诊时间: {doctor['schedule']}\n\n"
            
        logger.info("医生推荐完成")
        return result


class ScheduleAppointmentAction(BaseAction):
    """安排预约时间动作"""
    
    action_name = "ScheduleAppointment"
    action_desc = "查询并安排可用的预约时间"
    params_doc = {
        "doctor_id": "医生ID",
        "prefer_date": "偏好的日期（可选，格式：YYYY-MM-DD）",
        "prefer_time": "偏好的时间段（可选，如：上午、下午）"
    }
    
    def __call__(self, **kwargs):
        """执行安排预约时间动作"""
        logger.info(f"安排预约时间: {kwargs}")
        
        # 验证必要参数
        if "doctor_id" not in kwargs:
            error_msg = "缺少必要参数: doctor_id"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        doctor_id = kwargs.get("doctor_id")
        prefer_date = kwargs.get("prefer_date", None)
        prefer_time = kwargs.get("prefer_time", None)
        
        # 调用模拟的预约时间段数据服务
        try:
            slots = get_appointment_slots(doctor_id, prefer_date, prefer_time)
            logger.info(f"获取到 {len(slots)} 个可用预约时间段")
        except Exception as e:
            error_msg = f"获取预约时间段失败: {str(e)}"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        if not slots:
            no_result = "没有找到匹配的可用预约时间段"
            logger.warning(no_result)
            return no_result
        
        # 格式化预约时间段结果
        result = "以下是可用的预约时间段：\n\n"
        
        for slot in slots:
            result += f"- 日期: {slot['date']}, 时间: {slot['time']}\n"
            result += f"  医生: {slot['doctor_name']}\n"
            result += f"  科室: {slot['department']}\n"
            result += f"  地点: {slot['location']}\n"
            result += f"  挂号费: {slot['fee']} 元\n"
            result += f"  预约ID: {slot['slot_id']}\n\n"
            
        result += "请选择一个时间段进行预约，并使用预约ID进行确认。"
        
        logger.info("预约时间安排完成")
        return result


class ConfirmAppointmentAction(BaseAction):
    """确认预约信息动作"""
    
    action_name = "ConfirmAppointment"
    action_desc = "确认并完成预约"
    params_doc = {
        "slot_id": "预约时间段ID",
        "patient_name": "患者姓名",
        "patient_id": "患者ID或身份证号码",
        "contact": "联系方式"
    }
    
    def __call__(self, **kwargs):
        """执行确认预约动作"""
        logger.info(f"确认预约: {kwargs}")
        
        # 验证必要参数
        required_params = ["slot_id", "patient_name", "patient_id", "contact"]
        for param in required_params:
            if param not in kwargs:
                error_msg = f"缺少必要参数: {param}"
                logger.error(error_msg)
                return f"错误: {error_msg}"
        
        slot_id = kwargs.get("slot_id")
        patient_name = kwargs.get("patient_name")
        patient_id = kwargs.get("patient_id")
        contact = kwargs.get("contact")
        
        # 模拟预约确认逻辑
        # 在实际应用中，这里会调用预约服务API
        
        # 生成预约号
        import random
        appointment_id = f"APT{random.randint(100000, 999999)}"
        
        # 构建预约确认信息
        confirmation = {
            "appointment_id": appointment_id,
            "slot_id": slot_id,
            "patient_name": patient_name,
            "patient_id": patient_id,
            "contact": contact,
            "status": "已确认",
            "timestamp": "当前时间"  # 实际应用中使用实际时间戳
        }
        
        # 格式化预约确认结果
        result = "预约已成功确认！\n\n"
        result += f"预约号: {confirmation['appointment_id']}\n"
        result += f"患者: {confirmation['patient_name']}\n"
        result += f"身份证号: {patient_id[:6]}****{patient_id[-4:]}\n"  # 隐藏部分身份证号
        result += f"联系方式: {contact}\n"
        result += f"状态: {confirmation['status']}\n\n"
        
        result += "请在就诊当天提前30分钟到达医院，携带身份证和预约号。\n"
        result += "如需取消预约，请提前24小时联系医院。"
        
        logger.info(f"预约确认完成，预约号: {appointment_id}")
        return result
