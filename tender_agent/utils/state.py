from pydantic import BaseModel, Field
from typing import List, Dict, Type, Optional

class SimpleTenderAnalysis(BaseModel):
    """Анализ тендерной документации"""
    
    tender_type: str = Field(description="Тип тендера: закупка, обслуживание, ремонт, разработка")
    key_requirements: List[str] = Field(description="Ключевые требования к участнику")
    technical_specs: List[str] = Field(description="Технические характеристики и спецификации")
    budget: str = Field(description="Бюджет, цена или стоимость")
    deadlines: str = Field(description="Сроки выполнения и даты")

class AgentState(BaseModel):
    inp_file_path: str = Field(description='Путь к файлу для обработки')
    vectorstore_path: str = Field(description='Путь к векторной базе данных')

    context: List[str] = Field(description='Найденные релевантные данные для генерации ответа', default=[])

    answer_schema: Type[BaseModel] = Field(description="Схема выхожных данных", default=SimpleTenderAnalysis)
    search_queries: Dict[str, str] = Field(
        description = "Ключевые запросы для поиска в векторной базе данных",
        default = {
            "tender_type": "тип тендера закупка обслуживание ремонт поставка",
            "key_requirements": "требования к участнику лицензии опыт документы",
            "technical_specs": "технические характеристики спецификации ГОСТ ТУ параметры",
            "budget": "цена стоимость бюджет оплата НМЦК",
            "deadlines": "сроки выполнения дата окончания период график"
        }
    )
    output_path: str = Field()
    output: SimpleTenderAnalysis = Field(description="Ответ по тендерной документации", default=None)