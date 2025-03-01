"""
用户信息模型模块 - 负责管理用户基本信息和健康数据
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UserModel:
    """
    用户信息模型
    
    负责存储和管理用户的基本信息、健康数据和就诊历史
    """
    
    def __init__(self, user_id: str = None):
        """
        初始化用户信息模型
        
        Args:
            user_id: 用户ID，如果为None则自动生成
        """
        # 基本信息
        self.user_id = user_id if user_id else self._generate_user_id()
        self.basic_info = {
            "name": None,
            "gender": None,
            "age": None,
            "contact": None,
            "address": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 健康数据
        self.health_data = {
            "symptoms": [],              # 症状列表
            "medical_history": [],       # 病史记录
            "allergies": [],             # 过敏史
            "medications": [],           # 当前用药
            "chronic_conditions": []     # 慢性病情况
        }
        
        # 就诊历史
        self.medical_records = []
        
        # 对话上下文
        self.conversation_context = {}
        
        logger.info(f"用户模型初始化完成，用户ID: {self.user_id}")
        
    def _generate_user_id(self) -> str:
        """
        生成用户ID
        
        Returns:
            生成的用户ID
        """
        import uuid
        generated_id = f"user_{uuid.uuid4().hex[:8]}"
        logger.info(f"自动生成用户ID: {generated_id}")
        return generated_id
        
    def update_basic_info(self, info_dict: Dict[str, Any]) -> bool:
        """
        更新用户基本信息
        
        Args:
            info_dict: 包含用户基本信息的字典
            
        Returns:
            更新是否成功
        """
        logger.info(f"更新用户基本信息: {list(info_dict.keys())}")
        
        for key, value in info_dict.items():
            if key in self.basic_info:
                self.basic_info[key] = value
                logger.info(f"更新字段: {key} = {value}")
            else:
                logger.warning(f"未知字段: {key}，已忽略")
                
        # 更新时间戳
        self.basic_info["updated_at"] = datetime.now().isoformat()
        logger.info(f"用户信息更新时间: {self.basic_info['updated_at']}")
        
        return True
        
    def add_symptom(self, symptom: Dict[str, Any]) -> bool:
        """
        添加症状信息
        
        Args:
            symptom: 症状信息字典，包含症状描述、开始时间、严重程度等
            
        Returns:
            添加是否成功
        """
        if not isinstance(symptom, dict):
            logger.error(f"症状数据格式错误: {type(symptom)}")
            return False
            
        # 添加时间戳
        if "reported_at" not in symptom:
            symptom["reported_at"] = datetime.now().isoformat()
            
        # 添加症状ID
        if "symptom_id" not in symptom:
            import uuid
            symptom["symptom_id"] = f"sym_{uuid.uuid4().hex[:6]}"
            
        self.health_data["symptoms"].append(symptom)
        logger.info(f"添加症状信息: {symptom.get('description', '未知症状')}")
        
        return True
        
    def add_medical_history(self, history_item: Dict[str, Any]) -> bool:
        """
        添加病史记录
        
        Args:
            history_item: 病史记录字典，包含疾病名称、诊断时间、治疗方法等
            
        Returns:
            添加是否成功
        """
        if not isinstance(history_item, dict):
            logger.error(f"病史数据格式错误: {type(history_item)}")
            return False
            
        # 添加记录ID
        if "record_id" not in history_item:
            import uuid
            history_item["record_id"] = f"his_{uuid.uuid4().hex[:6]}"
            
        self.health_data["medical_history"].append(history_item)
        logger.info(f"添加病史记录: {history_item.get('disease', '未知疾病')}")
        
        return True
        
    def add_medical_record(self, record: Dict[str, Any]) -> bool:
        """
        添加就诊记录
        
        Args:
            record: 就诊记录字典，包含就诊时间、科室、医生、诊断结果等
            
        Returns:
            添加是否成功
        """
        if not isinstance(record, dict):
            logger.error(f"就诊记录格式错误: {type(record)}")
            return False
            
        # 添加记录ID和时间
        if "record_id" not in record:
            import uuid
            record["record_id"] = f"rec_{uuid.uuid4().hex[:6]}"
            
        if "created_at" not in record:
            record["created_at"] = datetime.now().isoformat()
            
        self.medical_records.append(record)
        logger.info(f"添加就诊记录: {record.get('department', '未知科室')} - {record.get('doctor', '未知医生')}")
        
        return True
        
    def update_conversation_context(self, context_dict: Dict[str, Any]) -> bool:
        """
        更新对话上下文
        
        Args:
            context_dict: 对话上下文字典
            
        Returns:
            更新是否成功
        """
        if not isinstance(context_dict, dict):
            logger.error(f"上下文数据格式错误: {type(context_dict)}")
            return False
            
        self.conversation_context.update(context_dict)
        logger.info(f"更新对话上下文: {list(context_dict.keys())}")
        
        return True
        
    def to_dict(self) -> Dict[str, Any]:
        """
        将用户模型转换为字典
        
        Returns:
            包含所有用户信息的字典
        """
        user_dict = {
            "user_id": self.user_id,
            "basic_info": self.basic_info,
            "health_data": self.health_data,
            "medical_records": self.medical_records,
            "conversation_context": self.conversation_context
        }
        
        logger.info(f"导出用户数据: {self.user_id}")
        return user_dict
        
    def from_dict(self, user_dict: Dict[str, Any]) -> bool:
        """
        从字典加载用户模型
        
        Args:
            user_dict: 包含用户信息的字典
            
        Returns:
            加载是否成功
        """
        try:
            # 验证字典结构
            required_keys = ["user_id", "basic_info", "health_data", "medical_records"]
            for key in required_keys:
                if key not in user_dict:
                    logger.error(f"用户数据缺少必要字段: {key}")
                    return False
                    
            # 加载数据
            self.user_id = user_dict["user_id"]
            self.basic_info = user_dict["basic_info"]
            self.health_data = user_dict["health_data"]
            self.medical_records = user_dict["medical_records"]
            
            # 加载上下文（如果有）
            if "conversation_context" in user_dict:
                self.conversation_context = user_dict["conversation_context"]
                
            logger.info(f"从字典加载用户数据成功: {self.user_id}")
            return True
            
        except Exception as e:
            logger.error(f"从字典加载用户数据失败: {str(e)}")
            return False
            
    def get_latest_symptoms(self, count: int = 3) -> List[Dict[str, Any]]:
        """
        获取最新的几条症状记录
        
        Args:
            count: 获取的记录数量
            
        Returns:
            最新的症状记录列表
        """
        # 按报告时间排序
        sorted_symptoms = sorted(
            self.health_data["symptoms"], 
            key=lambda x: x.get("reported_at", ""), 
            reverse=True
        )
        
        latest = sorted_symptoms[:count]
        logger.info(f"获取最新的 {len(latest)} 条症状记录")
        
        return latest
        
    def get_medical_summary(self) -> str:
        """
        生成用户健康状况摘要
        
        Returns:
            健康状况摘要文本
        """
        name = self.basic_info.get("name", "未知用户")
        gender = self.basic_info.get("gender", "未知")
        age = self.basic_info.get("age", "未知")
        
        summary = f"{name}，{gender}，{age}岁\n\n"
        
        # 添加当前症状
        latest_symptoms = self.get_latest_symptoms()
        if latest_symptoms:
            summary += "当前症状:\n"
            for sym in latest_symptoms:
                desc = sym.get("description", "未描述")
                duration = sym.get("duration", "未知")
                severity = sym.get("severity", "未知")
                summary += f"- {desc}，持续{duration}，严重程度: {severity}\n"
        else:
            summary += "当前无症状记录\n"
            
        # 添加病史
        if self.health_data["medical_history"]:
            summary += "\n病史:\n"
            for his in self.health_data["medical_history"][:3]:  # 最多显示3条
                disease = his.get("disease", "未知疾病")
                diagnosed_at = his.get("diagnosed_at", "未知时间")
                summary += f"- {disease} ({diagnosed_at})\n"
                
        # 添加过敏史
        if self.health_data["allergies"]:
            summary += "\n过敏史:\n"
            for allergy in self.health_data["allergies"]:
                if isinstance(allergy, dict):
                    allergen = allergy.get("allergen", "未知")
                    reaction = allergy.get("reaction", "未知反应")
                    summary += f"- {allergen}: {reaction}\n"
                else:
                    summary += f"- {allergy}\n"
                    
        # 添加当前用药
        if self.health_data["medications"]:
            summary += "\n当前用药:\n"
            for med in self.health_data["medications"]:
                if isinstance(med, dict):
                    name = med.get("name", "未知药物")
                    dosage = med.get("dosage", "未知剂量")
                    frequency = med.get("frequency", "未知频率")
                    summary += f"- {name}, {dosage}, {frequency}\n"
                else:
                    summary += f"- {med}\n"
        
        logger.info(f"生成用户健康状况摘要: {name}")
        return summary
        
    def get_appointment_history(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        获取最近的就诊记录
        
        Args:
            count: 获取的记录数量
            
        Returns:
            最近的就诊记录列表
        """
        # 按创建时间排序
        sorted_records = sorted(
            self.medical_records, 
            key=lambda x: x.get("created_at", ""), 
            reverse=True
        )
        
        latest = sorted_records[:count]
        logger.info(f"获取最近的 {len(latest)} 条就诊记录")
        
        return latest
