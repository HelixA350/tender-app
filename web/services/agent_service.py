from tender_agent.agent import agent
from tender_agent.utils.state import AgentState, technical_queries, TechnicalFields

class AgentService:
    """
    Сервис для работы с ИИ агентом
    """
    def __init__(self):
        self.analysis_type = {
            'tz': {
                'queries': technical_queries,
                'answer_schema': TechnicalFields,
            },
        }

    def call_agent(self, dir : str, analysis_type : str):
        """Вызов агента"""
        init_state = AgentState(
                inp_file_dir=dir,
                queries = self.analysis_type[analysis_type]['queries'],
                answer_schema=self.analysis_type[analysis_type]['answer_schema']
            )
        return agent.invoke(init_state)
