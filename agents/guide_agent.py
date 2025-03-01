"""
导诊推荐智能体模块 - 负责症状分析和科室匹配
"""
import logging
from typing import Dict, Any, List
from agentlite.agents import BaseAgent
from agentlite.actions import BaseAction

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GuideAgent(BaseAgent):
    """
    导诊推荐智能体
    
    负责采集症状信息，管理病史记录，进行智能科室匹配和医生专长匹配
    """
    
    def __init__(self, name: str, role: str, actions: List[BaseAction]):
        """
        初始化导诊推荐智能体
        
        Args:
            name: 智能体名称
            role: 智能体角色描述
            actions: 智能体可执行的动作列表
        """
        super().__init__(name=name, role=role, actions=actions)
        # 初始化症状信息存储
        self.symptom_info = {}
        # 初始化病史记录
        self.medical_history = {}
        # 初始化导诊状态
        self.guide_state = "初始化"
        logger.info(f"导诊推荐智能体 {name} 已初始化")
        
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
        你是一个专业的医院导诊助手。你需要根据用户的症状和病史，推荐合适的就诊科室和医生。
        
        用户请求: {instruction}
        
        请根据用户需求，完成以下任务：
        1. 采集详细的症状信息
        2. 了解用户的病史记录
        3. 根据症状和病史推荐合适的科室
        4. 根据科室和症状匹配专业医生
        
        当前已知症状：{self.symptom_info}
        当前已知病史：{self.medical_history}
        当前导诊状态：{self.guide_state}
        
        请确定下一步应该执行什么动作，可选的动作有：
        - CollectSymptoms: 采集症状信息
        - CollectMedicalHistory: 采集病史信息
        - AnalyzeHealthCondition: 分析健康状况
        - MatchDepartment: 匹配科室
        - MatchDoctor: 匹配医生
        - ProvideGuidance: 提供导诊建议
        
        请返回动作名称和必要的参数。
        """
        return prompt
    
    def process_symptom_info(self, symptom_dict: Dict[str, Any]) -> None:
        """
        处理并存储症状信息
        
        Args:
            symptom_dict: 症状信息字典
        """
        self.symptom_info.update(symptom_dict)
        logger.info(f"已更新症状信息: {list(symptom_dict.keys())}")
        
    def process_medical_history(self, history_dict: Dict[str, Any]) -> None:
        """
        处理并存储病史记录
        
        Args:
            history_dict: 病史信息字典
        """
        self.medical_history.update(history_dict)
        logger.info(f"已更新病史记录: {list(history_dict.keys())}")
        
    def update_guide_state(self, new_state: str) -> None:
        """
        更新导诊状态
        
        Args:
            new_state: 新的导诊状态
        """
        logger.info(f"导诊状态从 {self.guide_state} 更新为 {new_state}")
        self.guide_state = new_state
        
    def check_info_completeness(self) -> Dict[str, bool]:
        """
        检查症状和病史信息完整性
        
        Returns:
            各类信息的完整性状态
        """
        required_symptom_info = ["main_symptom", "duration", "severity"]
        required_history_info = ["past_diseases", "allergies", "medications"]
        
        symptom_info_complete = all(key in self.symptom_info for key in required_symptom_info)
        history_info_complete = all(key in self.medical_history for key in required_history_info)
        
        completeness = {
            "symptom_info": symptom_info_complete,
            "history_info": history_info_complete,
            "all_complete": symptom_info_complete and history_info_complete
        }
        
        logger.info(f"信息完整性检查: 症状信息={symptom_info_complete}, 病史信息={history_info_complete}")
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
