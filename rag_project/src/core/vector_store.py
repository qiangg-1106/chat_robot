import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from typing import List
from src.config.settings import settings

class VectorStoreManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model_name
        )
    
    def create_vector_store(self, documents: List[Document], save_path: str = None):
        """创建向量存储"""
        if not save_path:
            save_path = settings.vector_store_path
        
        # 确保存储目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        vector_store = FAISS.from_documents(documents, self.embeddings)
        vector_store.save_local(save_path)
        return vector_store
    
    def load_vector_store(self, load_path: str = None):
        """加载向量存储"""
        if not load_path:
            load_path = settings.vector_store_path
        
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"向量存储路径不存在: {load_path}")
        
        return FAISS.load_local(load_path, self.embeddings, allow_dangerous_deserialization=True)
    
    def get_retriever(self, vector_store=None):
        """获取检索器"""
        if not vector_store:
            vector_store = self.load_vector_store()
        
        return vector_store.as_retriever(
            search_kwargs={"k": settings.top_k_results}
        )

# 示例用法
if __name__ == "__main__":
    from document_processing import DocumentProcessor
    
    # 处理文档并创建向量存储
    processor = DocumentProcessor()
    docs = processor.process_documents("../data/raw/example.pdf")
    
    vs_manager = VectorStoreManager()
    vector_store = vs_manager.create_vector_store(docs)
    print("向量存储创建成功!")