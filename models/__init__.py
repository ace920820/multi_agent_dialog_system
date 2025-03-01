# models模块初始化文件
# 导出模块中的数据模型类，方便导入使用

from .user import UserModel
from .doctor import DoctorModel
from .department import DepartmentModel
from .appointment import AppointmentModel

__all__ = [
    'UserModel',
    'DoctorModel',
    'DepartmentModel',
    'AppointmentModel',
]
