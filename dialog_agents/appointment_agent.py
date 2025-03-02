"""
预约挂号智能体模块 - 负责处理预约挂号相关任务
"""
import logging
from typing import Dict, Any, List
from agentlite.agents import BaseAgent
from agentlite.actions import BaseAction

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AppointmentAgent(BaseAgent):
    """
    预约挂号智能体
    
    负责收集用户基本信息，了解就医需求，推荐合适科室和医生，并管理预约时间段
    """
    
    def __init__(self, name: str, role: str, actions: List[BaseAction], llm):
        """
        初始化预约挂号智能体
        
        Args:
            name: 智能体名称
            role: 智能体角色描述
            actions: 智能体可执行的动作列表
        """
        super().__init__(name=name, role=role, actions=actions, llm=llm)
        # 初始化用户信息存储
        self.user_info = {}
        # 初始化预约状态
        self.appointment_state = "初始化"
        logger.info(f"预约挂号智能体 {name} 已初始化")
        
    def generate_prompt(self, task_package: Dict[str, Any]) -> str:
        """
        根据任务包生成提示词
        
        Args:
            task_package: 任务包，包含任务指令和相关信息
            
        Returns:
            生成的提示词
        """
        instruction = task_package.get("instruction", "")
        logger.info(f"为任务生成提示词: {instruction[:20]}...")
        
        # 构建提示词
        prompt = f"""
        你是一个专业的医院预约挂号助手。你需要帮助用户完成预约挂号流程。
        
        用户请求: {instruction}
        
        请根据用户需求，完成以下任务：
        1. 收集用户基本信息（如姓名、性别、年龄、联系方式）
        2. 了解用户就医需求（症状描述、科室偏好、就医时间）
        3. 推荐合适的科室和医生
        4. 管理预约时间段
        
        当前已知信息：{self.user_info}
        当前预约状态：{self.appointment_state}
        
        请确定下一步应该执行什么动作，可选的动作有：
        - CollectUserInfo: 收集用户信息
        - AnalyzeSymptoms: 分析症状信息
        - RecommendDepartment: 推荐科室
        - RecommendDoctor: 推荐医生
        - ScheduleAppointment: 安排预约时间
        - ConfirmAppointment: 确认预约信息
        
        请返回动作名称和必要的参数。
        """
        return prompt
    
    def process_user_info(self, info_dict: Dict[str, Any]) -> None:
        """
        处理并存储用户信息
        
        Args:
            info_dict: 用户信息字典
        """
        self.user_info.update(info_dict)
        logger.info(f"已更新用户信息: {list(info_dict.keys())}")
        
    def update_appointment_state(self, new_state: str) -> None:
        """
        更新预约状态
        
        Args:
            new_state: 新的预约状态
        """
        logger.info(f"预约状态从 {self.appointment_state} 更新为 {new_state}")
        self.appointment_state = new_state
        
    def check_info_completeness(self) -> Dict[str, bool]:
        """
        检查用户信息完整性
        
        Returns:
            各类信息的完整性状态
        """
        required_basic_info = ["name", "gender", "age", "contact"]
        required_medical_info = ["symptoms", "preferred_department", "preferred_time"]
        
        basic_info_complete = all(key in self.user_info for key in required_basic_info)
        medical_info_complete = all(key in self.user_info for key in required_medical_info)
        
        completeness = {
            "basic_info": basic_info_complete,
            "medical_info": medical_info_complete,
            "all_complete": basic_info_complete and medical_info_complete
        }
        
        logger.info(f"信息完整性检查: 基本信息={basic_info_complete}, 医疗信息={medical_info_complete}")
        return completeness
        
    def run_action(self, action_str: str) -> str:
        """
        执行动作
        
        Args:
            action_str: 动作字符串，格式为 "动作名称: 参数1=值1, 参数2=值2, ..."
            
        Returns:
            动作执行结果
        """
        logger.info(f"执行动作: {action_str}")
        
        # 解析动作字符串
        action_parts = action_str.split(":", 1)
        action_name = action_parts[0].strip()
        
        # 解析参数
        params = {}
        if len(action_parts) > 1:
            params_str = action_parts[1].strip()
            for param in params_str.split(","):
                if "=" in param:
                    key, value = param.split("=", 1)
                    params[key.strip()] = value.strip()
        
        # 查找并执行相应的动作
        for action in self.actions:
            if action.action_name == action_name:
                logger.info(f"找到匹配的动作: {action_name}")
                result = action(**params)
                logger.info(f"动作执行完成: {action_name}")
                return result
                
        # 如果没有找到匹配的动作，返回错误信息
        error_msg = f"无法找到动作: {action_name}"
        logger.error(error_msg)
        return f"错误: {error_msg}"
