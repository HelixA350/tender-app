from tender_agent.utils.state import AgentState
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from files_loader import Loader
from langchain_community.llms.yandex import YandexGPT
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

def load_data(state : AgentState) -> AgentState:
    # Инициализация загрузчика и модели эмбеддингов
    loader = Loader(state.inp_file_dir)
    model_name = "ai-forever/ru-en-RoSBERTa"
    embeddings = HuggingFaceEmbeddings(model_name=model_name, show_progress=True)

    # Загрузка данных
    pages = []
    pages = loader.load_from_directory()
    pages = [doc for doc_list in pages.values() for doc in doc_list]

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
    queries = state.queries
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
    llm = YandexGPT(
        folder_id=os.environ.get('CATALOG_ID'),
        api_key=os.environ.get('YC_API_KEY'),
    )
    parser = JsonOutputParser(pydantic_object=state.answer_schema)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Ты — профессиональный аналитик тендерной документации. 
    Твоя задача — точно извлечь структурированную информацию из предоставленных фрагментов документации.

    КРИТИЧЕСКИ ВАЖНО:
    - Анализируй ТОЛЬКО предоставленные фрагменты документации
    - Не добавляй информацию, отсутствующую в исходном тексте
    - Будь максимально точен и объективен
    - В ответ в поле 'technical_specs' указывай подробно все технические требования
    - В ответ в поле 'key_requirements' указывай подробно все ключевые требования к участнику
    - Если информация по какому-либо полю не найдена, указывай "Не указано в документации
    - ОБЯЗАТЕЛЬНО форматируй ответ по следующей инструкции:
    {format_instructions}
         
         """),
    

        ("human", """ПРОАНАЛИЗИРУЙ СЛЕДУЮЩУЮ ТЕНДЕРНУЮ ДОКУМЕНТАЦИЮ И ИЗВЛЕКИ СТРУКТУРИРОВАННУЮ ИНФОРМАЦИЮ:

    {context}""")
    ])

    messages = prompt.invoke({"context": state.context,
                              "format_instructions": parser.get_format_instructions()})
    result = llm.invoke(messages)
    state.result = parser.parse(result)


    return state
