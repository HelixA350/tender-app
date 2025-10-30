from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
from langchain_community.llms.yandex import YandexGPT

load_dotenv()

# Инициализация модели эмбединга
model_name = "ai-forever/ru-en-RoSBERTa"
embeddings = HuggingFaceEmbeddings(model_name=model_name, show_progress=True)

# Инициализация разделителя текста на чанки
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=56,
    separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""],
    length_function=len,
    keep_separator=True
)

# Инициализация LLM
llm = YandexGPT(
    folder_id=os.environ.get('CATALOG_ID'),
    api_key=os.environ.get('YC_API_KEY'),
)
