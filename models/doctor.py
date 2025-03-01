"""
医生信息模型模块 - 负责管理医生信息数据
"""
import logging
from typing import Dict, List, Optional, Any

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DoctorModel:
    """
    医生信息模型
    
    负责存储和管理医生的基本信息、专业特长和排班信息
    """
    
    def __init__(self, doctor_id: str = None):
        """
        初始化医生信息模型
        
        Args:
            doctor_id: 医生ID，如果为None则自动生成
        """
        # 基本信息
        self.doctor_id = doctor_id if doctor_id else self._generate_doctor_id()
        self.basic_info = {
            "name": None,         # 姓名
            "gender": None,       # 性别
            "title": None,        # 职称
            "department_id": None, # 所属科室ID
            "department_name": None, # 所属科室名称
            "hospital": None,     # 所属医院
            "introduction": None  # 简介
        }
        
        # 专业特长
        self.specialties = []
        
        # 擅长疾病
        self.expertise = []
        
        # 排班信息
        self.schedules = []
        
        logger.info(f"医生模型初始化完成，医生ID: {self.doctor_id}")
        
    def _generate_doctor_id(self) -> str:
        """
        生成医生ID
        
        Returns:
            生成的医生ID
        """
        import uuid
        generated_id = f"doc_{uuid.uuid4().hex[:8]}"
        logger.info(f"自动生成医生ID: {generated_id}")
        return generated_id
        
    def update_basic_info(self, info_dict: Dict[str, Any]) -> bool:
        """
        更新医生基本信息
        
        Args:
            info_dict: 包含医生基本信息的字典
            
        Returns:
            更新是否成功
        """
        logger.info(f"更新医生基本信息: {list(info_dict.keys())}")
        
        for key, value in info_dict.items():
            if key in self.basic_info:
                self.basic_info[key] = value
                logger.info(f"更新字段: {key} = {value}")
            else:
                logger.warning(f"未知字段: {key}，已忽略")
                
        return True
        
    def add_specialty(self, specialty: str) -> bool:
        """
        添加专业特长
        
        Args:
            specialty: 专业特长描述
            
        Returns:
            添加是否成功
        """
        if specialty not in self.specialties:
            self.specialties.append(specialty)
            logger.info(f"添加专业特长: {specialty}")
            return True
        else:
            logger.info(f"专业特长已存在: {specialty}")
            return False
            
    def add_expertise(self, disease: str) -> bool:
        """
        添加擅长疾病
        
        Args:
            disease: 疾病名称
            
        Returns:
            添加是否成功
        """
        if disease not in self.expertise:
            self.expertise.append(disease)
            logger.info(f"添加擅长疾病: {disease}")
            return True
        else:
            logger.info(f"擅长疾病已存在: {disease}")
            return False
            
    def add_schedule(self, schedule: Dict[str, Any]) -> bool:
        """
        添加排班信息
        
        Args:
            schedule: 排班信息字典，包含日期、时段、可预约人数等
            
        Returns:
            添加是否成功
        """
        if not isinstance(schedule, dict):
            logger.error(f"排班数据格式错误: {type(schedule)}")
            return False
            
        # 验证必要字段
        required_fields = ["date", "time_slot"]
        for field in required_fields:
            if field not in schedule:
                logger.error(f"排班数据缺少必要字段: {field}")
                return False
                
        # 添加排班ID
        if "schedule_id" not in schedule:
            import uuid
            schedule["schedule_id"] = f"sch_{uuid.uuid4().hex[:6]}"
            
        # 检查是否已存在相同日期和时段的排班
        for existing in self.schedules:
            if (existing["date"] == schedule["date"] and 
                existing["time_slot"] == schedule["time_slot"]):
                logger.warning(f"排班已存在: {schedule['date']} {schedule['time_slot']}")
                return False
                
        self.schedules.append(schedule)
        logger.info(f"添加排班信息: {schedule['date']} {schedule['time_slot']}")
        
        return True
        
    def get_available_schedules(self, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取可预约的排班信息
        
        Args:
            date: 日期，如果为None则返回所有日期的可预约排班
            
        Returns:
            可预约的排班列表
        """
        available = []
        
        for schedule in self.schedules:
            # 检查日期匹配
            if date and schedule["date"] != date:
                continue
                
            # 检查是否仍有可预约名额
            if "available_slots" in schedule and schedule["available_slots"] > 0:
                available.append(schedule)
                
        logger.info(f"查询到 {len(available)} 条可预约排班信息" + (f" 于 {date}" if date else ""))
        return available
        
    def to_dict(self) -> Dict[str, Any]:
        """
        将医生模型转换为字典
        
        Returns:
            包含所有医生信息的字典
        """
        doctor_dict = {
            "doctor_id": self.doctor_id,
            "basic_info": self.basic_info,
            "specialties": self.specialties,
            "expertise": self.expertise,
            "schedules": self.schedules
        }
        
        logger.info(f"导出医生数据: {self.doctor_id}")
        return doctor_dict
        
    def from_dict(self, doctor_dict: Dict[str, Any]) -> bool:
        """
        从字典加载医生模型
        
        Args:
            doctor_dict: 包含医生信息的字典
            
        Returns:
            加载是否成功
        """
        try:
            # 验证字典结构
            required_keys = ["doctor_id", "basic_info"]
            for key in required_keys:
                if key not in doctor_dict:
                    logger.error(f"医生数据缺少必要字段: {key}")
                    return False
                    
            # 加载数据
            self.doctor_id = doctor_dict["doctor_id"]
            self.basic_info = doctor_dict["basic_info"]
            
            # 加载专业特长（如果有）
            if "specialties" in doctor_dict:
                self.specialties = doctor_dict["specialties"]
                
            # 加载擅长疾病（如果有）
            if "expertise" in doctor_dict:
                self.expertise = doctor_dict["expertise"]
                
            # 加载排班信息（如果有）
            if "schedules" in doctor_dict:
                self.schedules = doctor_dict["schedules"]
                
            logger.info(f"从字典加载医生数据成功: {self.doctor_id}")
            return True
            
        except Exception as e:
            logger.error(f"从字典加载医生数据失败: {str(e)}")
            return False
            
    def get_profile_summary(self) -> str:
        """
        生成医生简介摘要
        
        Returns:
            医生简介摘要文本
        """
        name = self.basic_info.get("name", "未知医生")
        title = self.basic_info.get("title", "")
        department = self.basic_info.get("department_name", "未知科室")
        hospital = self.basic_info.get("hospital", "未知医院")
        
        summary = f"{name} {title}\n{hospital} {department}\n\n"
        
        # 添加简介
        intro = self.basic_info.get("introduction", "")
        if intro:
            summary += f"简介：{intro}\n\n"
            
        # 添加专业特长
        if self.specialties:
            summary += "专业特长：\n"
            for specialty in self.specialties:
                summary += f"- {specialty}\n"
            summary += "\n"
            
        # 添加擅长疾病
        if self.expertise:
            summary += "擅长疾病：\n"
            for disease in self.expertise:
                summary += f"- {disease}\n"
                
        logger.info(f"生成医生简介摘要: {name}")
        return summary
