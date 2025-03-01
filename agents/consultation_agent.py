"""
医疗咨询智能体模块 - 负责健康问题解答和医疗建议
"""
import logging
from typing import Dict, Any, List
from agentlite.agents import BaseAgent
from agentlite.actions import BaseAction

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConsultationAgent(BaseAgent):
    """
    医疗咨询智能体
    
    负责提供健康问题解答、就医建议、用药指导和检查解读
    """
    
    def __init__(self, name: str, role: str, actions: List[BaseAction]):
        """
        初始化医疗咨询智能体
        
        Args:
            name: 智能体名称
            role: 智能体角色描述
            actions: 智能体可执行的动作列表
        """
        super().__init__(name=name, role=role, actions=actions)
        # 初始化咨询主题
        self.consultation_topic = None
        # 初始化咨询上下文
        self.consultation_context = {}
        # 初始化咨询状态
        self.consultation_state = "初始化"
        logger.info(f"医疗咨询智能体 {name} 已初始化")
        
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
        
        # 更新咨询主题（如果为空）
        if not self.consultation_topic:
            self._extract_consultation_topic(instruction)
            
        # 构建提示词
        prompt = f"""
        你是一个专业的医疗咨询助手。你需要根据用户的问题提供专业的医疗咨询和建议。
        
        用户请求: {instruction}
        
        请根据用户需求，完成以下任务：
        1. 解答用户的健康问题
        2. 提供专业的就医建议
        3. 根据情况提供用药指导
        4. 帮助用户理解医学检查结果（如有需要）
        
        当前咨询主题：{self.consultation_topic}
        当前咨询上下文：{self.consultation_context}
        当前咨询状态：{self.consultation_state}
        
        请确定下一步应该执行什么动作，可选的动作有：
        - AnalyzeHealthQuestion: 分析健康问题
        - ProvideHealthAdvice: 提供健康建议
        - ProvideMedicationGuidance: 提供用药指导
        - InterpretMedicalTest: 解读医学检查
        - SuggestFollowUpAction: 建议后续行动
        
        请返回动作名称和必要的参数。
        """
        return prompt
    
    def _extract_consultation_topic(self, instruction: str) -> None:
        """
        从用户指令中提取咨询主题
        
        Args:
            instruction: 用户指令
        """
        # 简单实现，实际应用中可能需要更复杂的逻辑
        lower_instruction = instruction.lower()
        
        if "头痛" in lower_instruction or "偏头痛" in lower_instruction:
            self.consultation_topic = "头痛问题"
        elif "胃痛" in lower_instruction or "腹痛" in lower_instruction:
            self.consultation_topic = "消化系统问题"
        elif "感冒" in lower_instruction or "发烧" in lower_instruction:
            self.consultation_topic = "感冒/发热问题"
        elif "皮疹" in lower_instruction or "皮肤" in lower_instruction:
            self.consultation_topic = "皮肤问题"
        elif "血压" in lower_instruction or "心脏" in lower_instruction:
            self.consultation_topic = "心血管问题"
        elif "药物" in lower_instruction or "用药" in lower_instruction:
            self.consultation_topic = "用药咨询"
        elif "检查" in lower_instruction or "报告" in lower_instruction:
            self.consultation_topic = "检查报告解读"
        else:
            self.consultation_topic = "一般健康咨询"
            
        logger.info(f"从用户指令中提取咨询主题: {self.consultation_topic}")
    
    def update_consultation_context(self, context_dict: Dict[str, Any]) -> None:
        """
        更新咨询上下文
        
        Args:
            context_dict: 上下文信息字典
        """
        self.consultation_context.update(context_dict)
        logger.info(f"已更新咨询上下文: {list(context_dict.keys())}")
        
    def update_consultation_state(self, new_state: str) -> None:
        """
        更新咨询状态
        
        Args:
            new_state: 新的咨询状态
        """
        logger.info(f"咨询状态从 {self.consultation_state} 更新为 {new_state}")
        self.consultation_state = new_state
        
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
