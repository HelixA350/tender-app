class AgentError(Exception):
    pass

class NoDocumentsError(AgentError):
    """Не удалось загрузить ни один документ из директории."""
    pass

class FailedToCreateVectorstoreError(AgentError):
    """Не удалось создать векторное хранилище."""
    pass

class LlmError(AgentError):
    """Ошибка при работе с LLM."""
    pass