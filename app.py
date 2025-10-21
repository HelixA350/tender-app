from tender_agent.agent import agent
from tender_agent.utils.state import AgentState

init_state = AgentState(
    inp_file_path=r"путь-к-PDF-файлу",
    vectorstore_path='./vectorstore',
    output_path='./result.json'
)

if __name__ == "__main__":
    agent.invoke(init_state)