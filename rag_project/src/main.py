import argparse
import os
import sys
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.document_processing import DocumentProcessor
from src.core.vector_store import VectorStoreManager
from src.core.generation import AnswerGenerator

def main():
    parser = argparse.ArgumentParser(description="RAG 智能问答系统")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 索引命令
    index_parser = subparsers.add_parser("index", help="创建文档索引")
    index_parser.add_argument("file_path", help="要处理的文档路径")
    index_parser.add_argument("--save_path", help="向量存储保存路径", default=None)
    
    # 问答命令
    query_parser = subparsers.add_parser("query", help="询问问题")
    query_parser.add_argument("question", help="要询问的问题")
    
    args = parser.parse_args()
    
    if args.command == "index":
        # 处理文档并创建索引
        print(f"正在处理文档: {args.file_path}")
        processor = DocumentProcessor()
        documents = processor.process_documents(args.file_path)
        
        vs_manager = VectorStoreManager()
        vs_manager.create_vector_store(documents, args.save_path)
        print("文档索引创建成功!")
        
    elif args.command == "query":
        # 进行问答
        vs_manager = VectorStoreManager()
        retriever = vs_manager.get_retriever()
        
        generator = AnswerGenerator()
        qa_chain = generator.create_qa_chain(retriever)
        
        result = qa_chain({"query": args.question})
        
        print("\n答案:", result["result"])
        print("\n来源文档:")
        for i, doc in enumerate(result["source_documents"]):
            print(f"{i+1}. {doc.page_content[:200]}...")
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 