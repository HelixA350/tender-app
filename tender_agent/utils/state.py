from pydantic import BaseModel, Field
from typing import List, Dict, Type

# --- Схемы данных для разных типов обработки ---
class analysisSchema(BaseModel):
    output_parameters: Type[BaseModel] = None
    queries: Dict[str, str] = {}

# - Анализ ТЗ -
class TechnicalFields(BaseModel):
    """Анализ тендерной документации"""
    
    tender_type: str = Field(description="Тип тендера: закупка, обслуживание, ремонт, разработка")
    key_requirements: List[str] = Field(description="Ключевые требования к участнику")
    technical_specs: List[str] = Field(description="Технические характеристики и спецификации")
    budget: str = Field(description="Бюджет, цена или стоимость")
    deadlines: str = Field(description="Сроки выполнения и даты")
class technical_analysis(analysisSchema):
    output_parameters: Type[BaseModel] = TechnicalFields
    queries: Dict[str, str] = {
            "tender_type": "тип тендера закупка обслуживание ремонт поставка",
            "key_requirements": "требования к участнику лицензии опыт документы",
            "technical_specs": "технические характеристики спецификации ГОСТ ТУ параметры",
            "budget": "цена стоимость бюджет оплата НМЦК",
            "deadlines": "сроки выполнения дата окончания период график"
    }



# --- Состояние агента ---
class AgentState(BaseModel):
    inp_file_dir: str = Field(description='Путь к папке с файлами для обработки')
    vectorstore_path: str = Field(description='Путь к векторной базе данных')

    context: List[str] = Field(description='Найденные релевантные данные для генерации ответа', default=[])

    analysis_schema: Type[analysisSchema] = Field(description='Тип схемы для анализа данных')
    output_path: str = Field()