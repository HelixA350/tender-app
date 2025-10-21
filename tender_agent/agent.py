from langgraph.graph import StateGraph, END, START
from tender_agent.utils.nodes import *
from tender_agent.utils.state import AgentState

agent_builder = StateGraph(AgentState)

# Узлы графа
agent_builder.add_node('load_data', load_data)
agent_builder.add_node('retrieve_date', retrieve_data)
agent_builder.add_node('generate_answer', generate_answer)

# Ребра графа
agent_builder.add_edge(START, 'load_data')
agent_builder.add_edge('load_data', 'retrieve_date')
agent_builder.add_edge('retrieve_date', 'generate_answer')
agent_builder.add_edge('generate_answer', END)

# Сборка графа
agent = agent_builder.compile()
agent.invoke


