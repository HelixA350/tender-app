from tender_agent.utils.state import AgentState
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_gigachat import GigaChat
import os
from langchain_core.prompts import ChatPromptTemplate
import json
from dotenv import load_dotenv

load_dotenv()


def load_data(state : AgentState) -> AgentState:
    # Инициализация загрузчика и модели эмбеддингов
    loader = PyPDFLoader(state.inp_file_path)
    model_name = "ai-forever/ru-en-RoSBERTa"
    embeddings = HuggingFaceEmbeddings(model_name=model_name, show_progress=True)

    # Загрузка данных
    pages = []
    pages = loader.load()

    # Разделение на чанки
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=56,
        separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""],
        length_function=len,
        keep_separator=True
    )
    pages = splitter.split_documents(pages)

    # Сохранение в векторном хранилище
    store = Chroma.from_documents(
        documents=pages,
        embedding=embeddings,
        persist_directory = state.vectorstore_path,
    )
    return state
    

def retrieve_data(state : AgentState) -> AgentState:
    all_chunks = []
    queries = state.search_queries
    model_name = "ai-forever/ru-en-RoSBERTa"
    embeddings = HuggingFaceEmbeddings(model_name=model_name, show_progress=True)
    store = Chroma(
        persist_directory=state.vectorstore_path,
        embedding_function=embeddings,
    )

    for field_name, query in queries.items():        
        # Ищем релевантные чанки в векторной БД
        relevant_docs = store.similarity_search(query, k=3)
        
        # Извлекаем текст из найденных документов
        for i, doc in enumerate(relevant_docs):
            chunk_text = doc.page_content
            all_chunks.append(chunk_text)

    unique_chunks = list(set(all_chunks))
    state.context = unique_chunks

    return state

def generate_answer(state : AgentState) -> AgentState:
    # Создаем LLM, выдающую структурированный ответ
    llm = GigaChat(
        credentials=os.getenv('AUTH_TOKEN'),
        verify_ssl_certs=False,
    )
    structured_llm = llm.with_structured_output(schema=state.answer_schema)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Ты — профессиональный аналитик тендерной документации. 
    Твоя задача — точно извлечь структурированную информацию из предоставленных фрагментов документации.

    КРИТИЧЕСКИ ВАЖНО:
    - Анализируй ТОЛЬКО предоставленные фрагменты документации
    - Не добавляй информацию, отсутствующую в исходном тексте
    - Будь максимально точен и объективен
    - Если информация по какому-либо полю не найдена, указывай "Не указано в документации"""),

        ("human", """ПРОАНАЛИЗИРУЙ СЛЕДУЮЩУЮ ТЕНДЕРНУЮ ДОКУМЕНТАЦИЮ И ИЗВЛЕКИ СТРУКТУРИРОВАННУЮ ИНФОРМАЦИЮ:

    {context}""")
    ])

    result = structured_llm.invoke(prompt.format(context=state.context))
    state.output = result

    with open(state.output_path, 'w', encoding='utf-8') as f:
        json.dump(result.dict(), f, ensure_ascii=False, indent=2)

    return state
