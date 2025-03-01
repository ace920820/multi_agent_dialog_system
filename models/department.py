"""
科室信息模型模块 - 负责管理医院科室信息
"""
import logging
from typing import Dict, List, Optional, Any

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DepartmentModel:
    """
    科室信息模型
    
    负责存储和管理科室的基本信息、医生列表和疾病类型
    """
    
    def __init__(self, department_id: str = None):
        """
        初始化科室信息模型
        
        Args:
            department_id: 科室ID，如果为None则自动生成
        """
        # 基本信息
        self.department_id = department_id if department_id else self._generate_department_id()
        self.basic_info = {
            "name": None,          # 科室名称
            "hospital": None,      # 所属医院
            "category": None,      # 科室分类（内科、外科等）
            "description": None,   # 科室描述
            "location": None       # 位置信息
        }
        
        # 医生列表（只存储医生ID和基本信息）
        self.doctors = []
        
        # 科室擅长疾病类型
        self.disease_types = []
        
        # 主要症状关键词
        self.symptom_keywords = []
        
        logger.info(f"科室模型初始化完成，科室ID: {self.department_id}")
        
    def _generate_department_id(self) -> str:
        """
        生成科室ID
        
        Returns:
            生成的科室ID
        """
        import uuid
        generated_id = f"dept_{uuid.uuid4().hex[:8]}"
        logger.info(f"自动生成科室ID: {generated_id}")
        return generated_id
        
    def update_basic_info(self, info_dict: Dict[str, Any]) -> bool:
        """
        更新科室基本信息
        
        Args:
            info_dict: 包含科室基本信息的字典
            
        Returns:
            更新是否成功
        """
        logger.info(f"更新科室基本信息: {list(info_dict.keys())}")
        
        for key, value in info_dict.items():
            if key in self.basic_info:
                self.basic_info[key] = value
                logger.info(f"更新字段: {key} = {value}")
            else:
                logger.warning(f"未知字段: {key}，已忽略")
                
        return True
        
    def add_doctor(self, doctor_info: Dict[str, Any]) -> bool:
        """
        添加医生到科室
        
        Args:
            doctor_info: 医生信息字典，必须包含doctor_id和name
            
        Returns:
            添加是否成功
        """
        # 验证必要字段
        if "doctor_id" not in doctor_info or "name" not in doctor_info:
            logger.error("医生信息缺少必要字段: doctor_id 或 name")
            return False
            
        # 检查是否已存在相同ID的医生
        doctor_id = doctor_info["doctor_id"]
        for doctor in self.doctors:
            if doctor["doctor_id"] == doctor_id:
                logger.warning(f"医生已存在于科室中: {doctor_id}")
                return False
                
        self.doctors.append(doctor_info)
        logger.info(f"添加医生到科室: {doctor_info.get('name', '未知医生')}")
        
        return True
        
    def remove_doctor(self, doctor_id: str) -> bool:
        """
        从科室移除医生
        
        Args:
            doctor_id: 医生ID
            
        Returns:
            移除是否成功
        """
        for i, doctor in enumerate(self.doctors):
            if doctor["doctor_id"] == doctor_id:
                removed = self.doctors.pop(i)
                logger.info(f"从科室移除医生: {removed.get('name', '未知医生')}")
                return True
                
        logger.warning(f"医生不在科室中: {doctor_id}")
        return False
        
    def add_disease_type(self, disease_type: str) -> bool:
        """
        添加科室擅长疾病类型
        
        Args:
            disease_type: 疾病类型描述
            
        Returns:
            添加是否成功
        """
        if disease_type not in self.disease_types:
            self.disease_types.append(disease_type)
            logger.info(f"添加科室擅长疾病类型: {disease_type}")
            return True
        else:
            logger.info(f"疾病类型已存在: {disease_type}")
            return False
            
    def add_symptom_keyword(self, keyword: str) -> bool:
        """
        添加症状关键词
        
        Args:
            keyword: 症状关键词
            
        Returns:
            添加是否成功
        """
        if keyword not in self.symptom_keywords:
            self.symptom_keywords.append(keyword)
            logger.info(f"添加症状关键词: {keyword}")
            return True
        else:
            logger.info(f"症状关键词已存在: {keyword}")
            return False
            
    def match_symptoms(self, symptoms: List[str]) -> float:
        """
        匹配症状与科室的相关度
        
        Args:
            symptoms: 症状描述列表
            
        Returns:
            匹配相关度评分 (0.0-1.0)
        """
        if not symptoms or not self.symptom_keywords:
            logger.warning("症状列表或科室关键词为空，无法匹配")
            return 0.0
            
        matched_count = 0
        
        for symptom in symptoms:
            # 简单的关键词匹配，实际应用中可能需要更复杂的NLP匹配算法
            for keyword in self.symptom_keywords:
                if keyword.lower() in symptom.lower():
                    matched_count += 1
                    break
                    
        # 计算相关度评分
        relevance = matched_count / len(symptoms) if symptoms else 0.0
        logger.info(f"症状与科室匹配相关度: {relevance:.2f} ({self.basic_info.get('name', '未知科室')})")
        
        return relevance
        
    def to_dict(self) -> Dict[str, Any]:
        """
        将科室模型转换为字典
        
        Returns:
            包含所有科室信息的字典
        """
        department_dict = {
            "department_id": self.department_id,
            "basic_info": self.basic_info,
            "doctors": self.doctors,
            "disease_types": self.disease_types,
            "symptom_keywords": self.symptom_keywords
        }
        
        logger.info(f"导出科室数据: {self.department_id}")
        return department_dict
        
    def from_dict(self, department_dict: Dict[str, Any]) -> bool:
        """
        从字典加载科室模型
        
        Args:
            department_dict: 包含科室信息的字典
            
        Returns:
            加载是否成功
        """
        try:
            # 验证字典结构
            required_keys = ["department_id", "basic_info"]
            for key in required_keys:
                if key not in department_dict:
                    logger.error(f"科室数据缺少必要字段: {key}")
                    return False
                    
            # 加载数据
            self.department_id = department_dict["department_id"]
            self.basic_info = department_dict["basic_info"]
            
            # 加载医生列表（如果有）
            if "doctors" in department_dict:
                self.doctors = department_dict["doctors"]
                
            # 加载疾病类型（如果有）
            if "disease_types" in department_dict:
                self.disease_types = department_dict["disease_types"]
                
            # 加载症状关键词（如果有）
            if "symptom_keywords" in department_dict:
                self.symptom_keywords = department_dict["symptom_keywords"]
                
            logger.info(f"从字典加载科室数据成功: {self.department_id}")
            return True
            
        except Exception as e:
            logger.error(f"从字典加载科室数据失败: {str(e)}")
            return False
            
    def get_department_summary(self) -> str:
        """
        生成科室摘要
        
        Returns:
            科室摘要文本
        """
        name = self.basic_info.get("name", "未知科室")
        hospital = self.basic_info.get("hospital", "未知医院")
        category = self.basic_info.get("category", "")
        
        summary = f"{name} ({category})\n{hospital}\n\n"
        
        # 添加描述
        description = self.basic_info.get("description", "")
        if description:
            summary += f"简介：{description}\n\n"
            
        # 添加位置信息
        location = self.basic_info.get("location", "")
        if location:
            summary += f"位置：{location}\n\n"
            
        # 添加擅长疾病类型
        if self.disease_types:
            summary += "擅长疾病类型：\n"
            for disease in self.disease_types:
                summary += f"- {disease}\n"
            summary += "\n"
            
        # 添加医生信息
        if self.doctors:
            summary += f"科室医生（{len(self.doctors)}名）：\n"
            for doctor in self.doctors[:5]:  # 最多显示5名医生
                name = doctor.get("name", "未知")
                title = doctor.get("title", "")
                summary += f"- {name} {title}\n"
                
            if len(self.doctors) > 5:
                summary += f"... 及其他 {len(self.doctors) - 5} 名医生\n"
                
        logger.info(f"生成科室摘要: {name}")
        return summary
