import os
from typing import List
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    WebBaseLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.config.settings import settings

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
    
    def load_documents(self, file_path: str) -> List[Document]:
        """根据文件扩展名加载文档"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        try:
            if ext == '.pdf':
                loader = PyPDFLoader(file_path)
            elif ext == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
            elif ext == '.md':
                loader = UnstructuredMarkdownLoader(file_path)
            else:
                raise ValueError(f"不支持的文件格式: {ext}")
            
            return loader.load()
        except Exception as e:
            raise Exception(f"文档加载失败: {str(e)}")
    
    def process_documents(self, file_path: str) -> List[Document]:
        """处理文档: 加载并分割"""
        documents = self.load_documents(file_path)
        return self.text_splitter.split_documents(documents)


if __name__ == "__main__":
    processor = DocumentProcessor()
    docs = processor.process_documents("../data/raw/example.pdf")
    print(f"加载了 {len(docs)} 个文档块")