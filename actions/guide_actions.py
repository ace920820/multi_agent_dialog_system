"""
导诊推荐动作模块 - 定义导诊推荐智能体可执行的动作
"""
import logging
from typing import Dict, Any
from agentlite.actions import BaseAction
from api.mock_data_service import get_symptom_analysis, get_medical_knowledge, get_department_matching

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CollectSymptomsAction(BaseAction):
    """采集症状信息动作"""
    
    action_name = "CollectSymptoms"
    action_desc = "采集用户的症状详细信息"
    params_doc = {
        "main_symptom": "主要症状",
        "duration": "症状持续时间",
        "severity": "症状严重程度",
        "related_symptoms": "相关伴随症状（可选）"
    }
    
    def __call__(self, **kwargs):
        """执行采集症状信息动作"""
        logger.info(f"采集症状信息: {kwargs}")
        
        # 验证必要参数
        required_params = ["main_symptom", "duration", "severity"]
        for param in required_params:
            if param not in kwargs:
                error_msg = f"缺少必要参数: {param}"
                logger.error(error_msg)
                return f"错误: {error_msg}"
        
        # 执行症状信息采集逻辑
        main_symptom = kwargs.get("main_symptom")
        duration = kwargs.get("duration")
        severity = kwargs.get("severity")
        related_symptoms = kwargs.get("related_symptoms", "无")
        
        # 构造采集结果
        collected_info = {
            "main_symptom": main_symptom,
            "duration": duration,
            "severity": severity,
            "related_symptoms": related_symptoms
        }
        
        # 返回采集结果
        result = f"已成功采集症状信息:\n"
        result += f"- 主要症状: {main_symptom}\n"
        result += f"- 持续时间: {duration}\n"
        result += f"- 严重程度: {severity}\n"
        result += f"- 相关症状: {related_symptoms}"
        
        logger.info("症状信息采集完成")
        return result


class CollectMedicalHistoryAction(BaseAction):
    """采集病史信息动作"""
    
    action_name = "CollectMedicalHistory"
    action_desc = "采集用户的病史记录信息"
    params_doc = {
        "past_diseases": "既往疾病史",
        "allergies": "过敏史",
        "medications": "用药史",
        "family_history": "家族病史（可选）"
    }
    
    def __call__(self, **kwargs):
        """执行采集病史信息动作"""
        logger.info(f"采集病史信息: {kwargs}")
        
        # 验证必要参数
        required_params = ["past_diseases", "allergies", "medications"]
        for param in required_params:
            if param not in kwargs:
                error_msg = f"缺少必要参数: {param}"
                logger.error(error_msg)
                return f"错误: {error_msg}"
        
        # 执行病史信息采集逻辑
        past_diseases = kwargs.get("past_diseases")
        allergies = kwargs.get("allergies")
        medications = kwargs.get("medications")
        family_history = kwargs.get("family_history", "无")
        
        # 构造采集结果
        collected_info = {
            "past_diseases": past_diseases,
            "allergies": allergies,
            "medications": medications,
            "family_history": family_history
        }
        
        # 返回采集结果
        result = f"已成功采集病史信息:\n"
        result += f"- 既往疾病史: {past_diseases}\n"
        result += f"- 过敏史: {allergies}\n"
        result += f"- 用药史: {medications}\n"
        result += f"- 家族病史: {family_history}"
        
        logger.info("病史信息采集完成")
        return result


class AnalyzeHealthConditionAction(BaseAction):
    """分析健康状况动作"""
    
    action_name = "AnalyzeHealthCondition"
    action_desc = "分析用户的健康状况，结合症状和病史"
    params_doc = {
        "main_symptom": "主要症状",
        "related_symptoms": "相关症状",
        "past_diseases": "既往疾病史",
        "age": "年龄（可选）",
        "gender": "性别（可选）"
    }
    
    def __call__(self, **kwargs):
        """执行分析健康状况动作"""
        logger.info(f"分析健康状况: {kwargs}")
        
        # 验证必要参数
        if "main_symptom" not in kwargs:
            error_msg = "缺少必要参数: main_symptom"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        # 获取参数
        main_symptom = kwargs.get("main_symptom")
        related_symptoms = kwargs.get("related_symptoms", "无")
        past_diseases = kwargs.get("past_diseases", "无")
        age = kwargs.get("age", "未知")
        gender = kwargs.get("gender", "未知")
        
        # 调用模拟的症状分析服务
        try:
            analysis = get_symptom_analysis(main_symptom, related_symptoms, past_diseases, age, gender)
            logger.info("获取症状分析结果成功")
        except Exception as e:
            error_msg = f"获取症状分析失败: {str(e)}"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        if not analysis:
            no_result = "无法分析当前健康状况，信息不足"
            logger.warning(no_result)
            return no_result
        
        # 格式化分析结果
        result = "健康状况分析结果：\n\n"
        
        result += f"根据您提供的信息：\n"
        result += f"- 主要症状: {main_symptom}\n"
        result += f"- 相关症状: {related_symptoms}\n"
        result += f"- 既往疾病: {past_diseases}\n"
        if age != "未知":
            result += f"- 年龄: {age}\n"
        if gender != "未知":
            result += f"- 性别: {gender}\n"
        
        result += f"\n初步分析：\n{analysis['analysis']}\n\n"
        
        if "possible_conditions" in analysis:
            result += "可能的健康状况：\n"
            for condition in analysis["possible_conditions"]:
                result += f"- {condition}\n"
        
        if "risk_level" in analysis:
            result += f"\n风险等级: {analysis['risk_level']}\n"
            
        if "recommendations" in analysis:
            result += "\n建议：\n"
            for rec in analysis["recommendations"]:
                result += f"- {rec}\n"
        
        logger.info("健康状况分析完成")
        return result


class MatchDepartmentAction(BaseAction):
    """匹配科室动作"""
    
    action_name = "MatchDepartment"
    action_desc = "根据症状和健康状况匹配适合的就诊科室"
    params_doc = {
        "main_symptom": "主要症状",
        "possible_conditions": "可能的健康状况",
        "previous_treatment": "之前的治疗经历（可选）"
    }
    
    def __call__(self, **kwargs):
        """执行匹配科室动作"""
        logger.info(f"匹配科室: {kwargs}")
        
        # 验证必要参数
        if "main_symptom" not in kwargs:
            error_msg = "缺少必要参数: main_symptom"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        # 获取参数
        main_symptom = kwargs.get("main_symptom")
        possible_conditions = kwargs.get("possible_conditions", "未知")
        previous_treatment = kwargs.get("previous_treatment", "无")
        
        # 调用模拟的科室匹配服务
        try:
            departments = get_department_matching(main_symptom, possible_conditions)
            logger.info(f"获取到 {len(departments)} 个匹配的科室")
        except Exception as e:
            error_msg = f"获取科室匹配失败: {str(e)}"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        if not departments:
            no_result = "没有找到匹配的科室，建议先去内科进行初步诊断"
            logger.warning(no_result)
            return no_result
        
        # 格式化匹配结果
        result = "根据您的症状和可能的情况，为您匹配到以下科室：\n\n"
        
        for dept in departments:
            result += f"- {dept['name']}\n"
            result += f"  适用症状: {dept['applicable_symptoms']}\n"
            result += f"  处理疾病: {dept['handled_conditions']}\n"
            result += f"  匹配度: {dept['match_score']}%\n"
            if "description" in dept:
                result += f"  科室说明: {dept['description']}\n"
            result += "\n"
            
        result += "建议您根据症状的严重程度和匹配度选择合适的科室就诊。\n"
        if previous_treatment != "无":
            result += f"考虑到您之前的治疗经历（{previous_treatment}），您可能需要优先考虑这方面的专科医生。"
        
        logger.info("科室匹配完成")
        return result


class MatchDoctorAction(BaseAction):
    """匹配医生动作"""
    
    action_name = "MatchDoctor"
    action_desc = "在匹配的科室中推荐合适的医生"
    params_doc = {
        "department": "科室名称",
        "specific_condition": "具体病情",
        "prefer_expertise": "偏好的专长（可选）",
        "prefer_gender": "偏好的医生性别（可选）"
    }
    
    def __call__(self, **kwargs):
        """执行匹配医生动作"""
        # 此函数逻辑与appointment_actions.py中的RecommendDoctorAction类似
        # 为了避免重复，这里可以调用那个动作或实现类似逻辑
        # 这里略去实现，实际应用中应该完整实现
        logger.info(f"匹配医生: {kwargs}")
        
        # 验证必要参数
        if "department" not in kwargs:
            error_msg = "缺少必要参数: department"
            logger.error(error_msg)
            return f"错误: {error_msg}"
        
        department = kwargs.get("department")
        specific_condition = kwargs.get("specific_condition", "未指定")
        prefer_expertise = kwargs.get("prefer_expertise", None)
        prefer_gender = kwargs.get("prefer_gender", None)
        
        # 模拟医生匹配结果
        result = f"根据您的需求，为您在{department}科匹配到以下医生：\n\n"
        
        # 模拟几位医生的信息
        doctors = [
            {
                "name": "张医生",
                "gender": "男",
                "title": "主任医师",
                "expertise": "专长于复杂疑难病例的诊断和治疗",
                "rating": 4.9,
                "experience": "30年临床经验",
                "match_reason": "擅长处理您描述的症状",
                "available": "周一、周三上午"
            },
            {
                "name": "李医生",
                "gender": "女",
                "title": "副主任医师",
                "expertise": "专长于慢性病的管理和治疗",
                "rating": 4.8,
                "experience": "25年临床经验",
                "match_reason": "对您的具体病情有丰富的治疗经验",
                "available": "周二、周四全天"
            }
        ]
        
        # 根据偏好筛选
        filtered_doctors = doctors
        if prefer_gender:
            filtered_doctors = [d for d in filtered_doctors if d["gender"] == prefer_gender]
        
        # 如果筛选后没有结果，使用原始列表
        if not filtered_doctors:
            filtered_doctors = doctors
            
        # 格式化医生信息
        for doctor in filtered_doctors:
            result += f"- {doctor['name']} ({doctor['gender']}), {doctor['title']}\n"
            result += f"  专长: {doctor['expertise']}\n"
            result += f"  经验: {doctor['experience']}\n"
            result += f"  评分: {doctor['rating']}/5.0\n"
            result += f"  匹配原因: {doctor['match_reason']}\n"
            result += f"  出诊时间: {doctor['available']}\n\n"
        
        logger.info(f"医生匹配完成，找到 {len(filtered_doctors)} 位匹配的医生")
        return result


class ProvideGuidanceAction(BaseAction):
    """提供导诊建议动作"""
    
    action_name = "ProvideGuidance"
    action_desc = "根据用户情况提供全面的导诊建议"
    params_doc = {
        "symptoms": "症状信息",
        "suggested_department": "建议的科室",
        "suggested_doctor": "建议的医生（可选）",
        "urgency_level": "紧急程度（可选）"
    }
    
    def __call__(self, **kwargs):
        """执行提供导诊建议动作"""
        logger.info(f"提供导诊建议: {kwargs}")
        
        # 验证必要参数
        required_params = ["symptoms", "suggested_department"]
        for param in required_params:
            if param not in kwargs:
                error_msg = f"缺少必要参数: {param}"
                logger.error(error_msg)
                return f"错误: {error_msg}"
        
        # 获取参数
        symptoms = kwargs.get("symptoms")
        suggested_department = kwargs.get("suggested_department")
        suggested_doctor = kwargs.get("suggested_doctor", "未指定")
        urgency_level = kwargs.get("urgency_level", "常规")
        
        # 尝试获取相关医学知识
        try:
            knowledge = get_medical_knowledge(symptoms)
            has_knowledge = True
            logger.info("获取相关医学知识成功")
        except Exception:
            knowledge = None
            has_knowledge = False
            logger.warning("获取相关医学知识失败")
        
        # 构建导诊建议
        result = "【导诊建议】\n\n"
        
        # 根据紧急程度给出建议
        if urgency_level.lower() in ["紧急", "急诊", "高"]:
            result += "⚠️ 您的情况可能需要紧急医疗干预，建议立即前往医院急诊科就诊。\n\n"
        
        # 主要建议
        result += f"根据您描述的症状（{symptoms}），建议您:\n\n"
        result += f"1. 就诊科室: {suggested_department}\n"
        
        if suggested_doctor != "未指定":
            result += f"2. 推荐医生: {suggested_doctor}\n"
            
        result += f"3. 就诊准备:\n"
        result += f"   - 带好个人身份证件\n"
        result += f"   - 准备好详细的症状描述，包括发作时间、持续时长、缓解因素等\n"
        result += f"   - 若有之前的检查报告、用药记录，请一并带上\n"
        
        # 添加相关医学知识（如果有）
        if has_knowledge and knowledge:
            result += f"\n相关医学知识:\n{knowledge}\n"
        
        # 就诊流程指导
        result += f"\n就诊流程:\n"
        result += f"1. 到医院挂号处挂{suggested_department}号\n"
        result += f"2. 按照导诊台指引前往候诊区等候\n"
        result += f"3. 医生问诊时，清晰描述您的症状和不适\n"
        result += f"4. 根据医生建议，可能需要进行相关检查\n"
        result += f"5. 复诊时带上检查结果和之前的病历\n"
        
        # 根据紧急程度添加注意事项
        if urgency_level.lower() in ["紧急", "急诊", "高"]:
            result += f"\n⚠️ 注意事项: 考虑到您情况的紧急性，请尽快就医，必要时可拨打急救电话（120）。\n"
        else:
            result += f"\n注意事项: 若症状加重，请及时调整就诊计划，必要时前往急诊科。\n"
        
        logger.info("导诊建议提供完成")
        return result
