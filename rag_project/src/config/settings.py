import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # 嵌入模型设置
    embedding_model_name: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    # LLM 模型设置
    llm_model_name: str = os.getenv("LLM_MODEL_NAME", "gpt2")
    
    # 向量存储设置
    vector_store_path: str = os.getenv("VECTOR_STORE_PATH", "./storage/faiss_index")
    
    # 文本分割设置
    chunk_size: int = int(os.getenv("CHUNK_SIZE", 500))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", 100))
    
    # 检索设置
    top_k_results: int = int(os.getenv("TOP_K_RESULTS", 3))

settings = Settings()