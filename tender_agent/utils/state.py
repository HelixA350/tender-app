from pydantic import BaseModel, Field
from typing import List, Dict, Type, Optional

# --- Схемы данных ---
class TechnicalFields(BaseModel):
    """Выходные данные, которые необходимо извлечь из текста технического задания тендерной документации"""
    tender_type: str = Field(description="Тип тендера: закупка, обслуживание, ремонт, разработка")
    key_requirements: List[str] = Field(description="Ключевые требования к участнику")
    technical_specs: List[str] = Field(description="Технические требования к работе")
    budget: str = Field(description="Бюджет, цена или стоимость")
    deadlines: str = Field(description="Сроки выполнения и даты")


technical_queries={
    "tender_type": "тип тендера закупка обслуживание ремонт поставка",
    "key_requirements": "требования к участнику лицензии опыт документы",
    "technical_specs": "технические характеристики спецификации ГОСТ ТУ параметры",
    "budget": "цена стоимость бюджет оплата НМЦК",
    "deadlines": "сроки выполнения дата окончания период график"
}


# --- Состояние агента ---
class AgentState(BaseModel):
    inp_file_dir: str = Field(description='Путь к папке с файлами для обработки')
    vectorstore_path: str = Field(description='Путь к векторной базе данных', default='vectorstore')
    context: List[str] = Field(default=[], description='Найденные релевантные данные')
    queries: Dict[str, str] = Field(description='Запросы для поиска')
    answer_schema: Type[BaseModel] = Field(description='Схема выходных данных')
    result: Optional[Type[BaseModel]] = Field(description='Результат обработки', default=None)