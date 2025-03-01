"""
预约信息模型模块 - 负责管理用户预约信息
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AppointmentModel:
    """
    预约信息模型
    
    负责存储和管理用户的预约信息，包括预约状态跟踪和历史记录
    """
    
    # 预约状态枚举
    STATUS_PENDING = "pending"    # 待确认
    STATUS_CONFIRMED = "confirmed"  # 已确认
    STATUS_CANCELED = "canceled"   # 已取消
    STATUS_COMPLETED = "completed"  # 已完成
    
    def __init__(self, appointment_id: str = None):
        """
        初始化预约信息模型
        
        Args:
            appointment_id: 预约ID，如果为None则自动生成
        """
        # 基本信息
        self.appointment_id = appointment_id if appointment_id else self._generate_appointment_id()
        self.appointment_info = {
            "user_id": None,            # 用户ID
            "doctor_id": None,          # 医生ID
            "department_id": None,      # 科室ID
            "date": None,               # 预约日期
            "time_slot": None,          # 预约时段
            "symptom_description": "",  # 症状描述
            "appointment_type": "consultation",  # 预约类型（问诊、复诊等）
            "status": self.STATUS_PENDING,  # 预约状态
            "created_at": datetime.now().isoformat(),  # 创建时间
            "updated_at": datetime.now().isoformat()   # 更新时间
        }
        
        # 预约状态历史
        self.status_history = [{
            "status": self.STATUS_PENDING,
            "timestamp": datetime.now().isoformat(),
            "remark": "预约创建"
        }]
        
        # 备注信息
        self.remarks = []
        
        logger.info(f"预约模型初始化完成，预约ID: {self.appointment_id}")
        
    def _generate_appointment_id(self) -> str:
        """
        生成预约ID
        
        Returns:
            生成的预约ID
        """
        import uuid
        generated_id = f"appt_{uuid.uuid4().hex[:8]}"
        logger.info(f"自动生成预约ID: {generated_id}")
        return generated_id
        
    def update_appointment_info(self, info_dict: Dict[str, Any]) -> bool:
        """
        更新预约信息
        
        Args:
            info_dict: 包含预约信息的字典
            
        Returns:
            更新是否成功
        """
        logger.info(f"更新预约信息: {list(info_dict.keys())}")
        
        # 记录原状态用于检测状态变化
        old_status = self.appointment_info.get("status")
        
        for key, value in info_dict.items():
            if key in self.appointment_info:
                self.appointment_info[key] = value
                logger.info(f"更新字段: {key} = {value}")
            else:
                logger.warning(f"未知字段: {key}，已忽略")
                
        # 更新时间戳
        self.appointment_info["updated_at"] = datetime.now().isoformat()
        
        # 如果状态发生变化，记录状态历史
        new_status = self.appointment_info.get("status")
        if old_status != new_status and new_status:
            self.add_status_history(new_status, f"状态从 {old_status} 更改为 {new_status}")
            
        return True
        
    def confirm_appointment(self, remark: str = "预约已确认") -> bool:
        """
        确认预约
        
        Args:
            remark: 备注信息
            
        Returns:
            操作是否成功
        """
        current_status = self.appointment_info.get("status")
        
        if current_status != self.STATUS_PENDING:
            logger.warning(f"只有待确认状态的预约可以被确认，当前状态: {current_status}")
            return False
            
        self.appointment_info["status"] = self.STATUS_CONFIRMED
        self.appointment_info["updated_at"] = datetime.now().isoformat()
        
        # 添加状态历史
        self.add_status_history(self.STATUS_CONFIRMED, remark)
        
        logger.info(f"预约已确认: {self.appointment_id}")
        return True
        
    def cancel_appointment(self, remark: str = "预约已取消") -> bool:
        """
        取消预约
        
        Args:
            remark: 取消原因
            
        Returns:
            操作是否成功
        """
        current_status = self.appointment_info.get("status")
        
        if current_status not in [self.STATUS_PENDING, self.STATUS_CONFIRMED]:
            logger.warning(f"只有待确认或已确认状态的预约可以被取消，当前状态: {current_status}")
            return False
            
        self.appointment_info["status"] = self.STATUS_CANCELED
        self.appointment_info["updated_at"] = datetime.now().isoformat()
        
        # 添加状态历史和备注
        self.add_status_history(self.STATUS_CANCELED, remark)
        
        logger.info(f"预约已取消: {self.appointment_id}")
        return True
        
    def complete_appointment(self, remark: str = "预约已完成") -> bool:
        """
        完成预约
        
        Args:
            remark: 备注信息
            
        Returns:
            操作是否成功
        """
        current_status = self.appointment_info.get("status")
        
        if current_status != self.STATUS_CONFIRMED:
            logger.warning(f"只有已确认状态的预约可以被标记为完成，当前状态: {current_status}")
            return False
            
        self.appointment_info["status"] = self.STATUS_COMPLETED
        self.appointment_info["updated_at"] = datetime.now().isoformat()
        
        # 添加状态历史
        self.add_status_history(self.STATUS_COMPLETED, remark)
        
        logger.info(f"预约已完成: {self.appointment_id}")
        return True
        
    def add_status_history(self, status: str, remark: str = "") -> bool:
        """
        添加状态历史记录
        
        Args:
            status: 状态
            remark: 备注信息
            
        Returns:
            添加是否成功
        """
        status_record = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "remark": remark
        }
        
        self.status_history.append(status_record)
        logger.info(f"添加状态历史: {status} - {remark}")
        
        return True
        
    def add_remark(self, remark: str) -> bool:
        """
        添加备注信息
        
        Args:
            remark: 备注内容
            
        Returns:
            添加是否成功
        """
        remark_record = {
            "content": remark,
            "timestamp": datetime.now().isoformat()
        }
        
        self.remarks.append(remark_record)
        logger.info(f"添加备注: {remark}")
        
        return True
        
    def to_dict(self) -> Dict[str, Any]:
        """
        将预约模型转换为字典
        
        Returns:
            包含所有预约信息的字典
        """
        appointment_dict = {
            "appointment_id": self.appointment_id,
            "appointment_info": self.appointment_info,
            "status_history": self.status_history,
            "remarks": self.remarks
        }
        
        logger.info(f"导出预约数据: {self.appointment_id}")
        return appointment_dict
        
    def from_dict(self, appointment_dict: Dict[str, Any]) -> bool:
        """
        从字典加载预约模型
        
        Args:
            appointment_dict: 包含预约信息的字典
            
        Returns:
            加载是否成功
        """
        try:
            # 验证字典结构
            required_keys = ["appointment_id", "appointment_info"]
            for key in required_keys:
                if key not in appointment_dict:
                    logger.error(f"预约数据缺少必要字段: {key}")
                    return False
                    
            # 加载数据
            self.appointment_id = appointment_dict["appointment_id"]
            self.appointment_info = appointment_dict["appointment_info"]
            
            # 加载状态历史（如果有）
            if "status_history" in appointment_dict:
                self.status_history = appointment_dict["status_history"]
                
            # 加载备注信息（如果有）
            if "remarks" in appointment_dict:
                self.remarks = appointment_dict["remarks"]
                
            logger.info(f"从字典加载预约数据成功: {self.appointment_id}")
            return True
            
        except Exception as e:
            logger.error(f"从字典加载预约数据失败: {str(e)}")
            return False
            
    def get_appointment_summary(self) -> str:
        """
        生成预约摘要信息
        
        Returns:
            预约摘要文本
        """
        date = self.appointment_info.get("date", "未定")
        time_slot = self.appointment_info.get("time_slot", "未定")
        doctor_id = self.appointment_info.get("doctor_id", "未定")
        dept_id = self.appointment_info.get("department_id", "未定")
        status = self.appointment_info.get("status", "未知")
        
        status_display = {
            self.STATUS_PENDING: "待确认",
            self.STATUS_CONFIRMED: "已确认",
            self.STATUS_CANCELED: "已取消",
            self.STATUS_COMPLETED: "已完成"
        }.get(status, status)
        
        summary = f"预约ID: {self.appointment_id}\n"
        summary += f"预约时间: {date} {time_slot}\n"
        summary += f"科室ID: {dept_id}\n"
        summary += f"医生ID: {doctor_id}\n"
        summary += f"状态: {status_display}\n\n"
        
        # 添加症状描述
        symptom = self.appointment_info.get("symptom_description", "")
        if symptom:
            summary += f"症状描述: {symptom}\n\n"
            
        # 添加最近的状态变更
        if self.status_history and len(self.status_history) > 1:
            latest = self.status_history[-1]
            timestamp = latest.get("timestamp", "")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass
            status = latest.get("status", "")
            status_display = {
                self.STATUS_PENDING: "待确认",
                self.STATUS_CONFIRMED: "已确认",
                self.STATUS_CANCELED: "已取消",
                self.STATUS_COMPLETED: "已完成"
            }.get(status, status)
            remark = latest.get("remark", "")
            
            summary += f"最近状态变更: {status_display} ({timestamp})\n"
            if remark:
                summary += f"备注: {remark}\n"
                
        logger.info(f"生成预约摘要: {self.appointment_id}")
        return summary
        
    def is_conflict_with(self, other_appointment: Dict[str, Any]) -> bool:
        """
        检查与另一个预约是否冲突
        
        Args:
            other_appointment: 另一个预约的信息字典
            
        Returns:
            是否存在冲突
        """
        # 仅检查当前有效的预约（待确认和已确认状态）
        if self.appointment_info["status"] not in [self.STATUS_PENDING, self.STATUS_CONFIRMED]:
            logger.info(f"当前预约状态为 {self.appointment_info['status']}，不检查冲突")
            return False
            
        # 检查日期和时间段是否重叠
        if (self.appointment_info["date"] == other_appointment.get("date") and 
            self.appointment_info["time_slot"] == other_appointment.get("time_slot")):
            
            # 检查是否为同一个医生
            if self.appointment_info["doctor_id"] == other_appointment.get("doctor_id"):
                logger.warning(f"发现预约冲突: 相同医生在相同时间段已有预约")
                return True
                
            # 检查是否为同一个用户
            if self.appointment_info["user_id"] == other_appointment.get("user_id"):
                logger.warning(f"发现预约冲突: 用户在相同时间段已有其他预约")
                return True
                
        return False
