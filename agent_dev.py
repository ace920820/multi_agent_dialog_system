from agentlite.agents import BaseAgent
from agentlite.llm import agent_llms,LLMConfig
name = "agent_name"
role = "describe the roles of this agent"
actions = ['Action1', 'Action2']
LLMConfig = LLMConfig({})
llm = agent_llms.BaseLLM(llm_config = LLMConfig)
agent = BaseAgent(name=name, role=role, actions=actions,llm=llm)