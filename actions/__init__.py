# actions模块初始化文件
# 导出模块中的动作类，方便导入使用

from .appointment_actions import (
    CollectUserInfoAction,
    AnalyzeSymptomsAction,
    RecommendDepartmentAction,
    RecommendDoctorAction,
    ScheduleAppointmentAction,
    ConfirmAppointmentAction
)

from .guide_actions import (
    CollectSymptomsAction,
    CollectMedicalHistoryAction,
    AnalyzeHealthConditionAction,
    MatchDepartmentAction,
    MatchDoctorAction,
    ProvideGuidanceAction
)

from .consultation_actions import (
    AnalyzeHealthQuestionAction,
    ProvideHealthAdviceAction,
    ProvideMedicationGuidanceAction,
    InterpretMedicalTestAction,
    SuggestFollowUpActionAction
)

__all__ = [
    # 预约挂号动作
    'CollectUserInfoAction',
    'AnalyzeSymptomsAction',
    'RecommendDepartmentAction',
    'RecommendDoctorAction',
    'ScheduleAppointmentAction',
    'ConfirmAppointmentAction',
    
    # 导诊推荐动作
    'CollectSymptomsAction',
    'CollectMedicalHistoryAction',
    'AnalyzeHealthConditionAction',
    'MatchDepartmentAction',
    'MatchDoctorAction',
    'ProvideGuidanceAction',
    
    # 医疗咨询动作
    'AnalyzeHealthQuestionAction',
    'ProvideHealthAdviceAction',
    'ProvideMedicationGuidanceAction',
    'InterpretMedicalTestAction',
    'SuggestFollowUpActionAction'
]
