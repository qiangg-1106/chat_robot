from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import pipeline
from src.config.settings import settings

class AnswerGenerator:
    def __init__(self):
        self.llm = self._load_llm()
        self.prompt_template = self._create_prompt_template()
    
    def _load_llm(self):
        """加载语言模型"""
        try:
            # 使用 Hugging Face 管道
            llm_pipeline = pipeline(
                "text-generation",
                model=settings.llm_model_name,
                max_new_tokens=200,
                temperature=0.1
            )
            return HuggingFacePipeline(pipeline=llm_pipeline)
        except Exception as e:
            raise Exception(f"模型加载失败: {str(e)}")
    
    def _create_prompt_template(self):
        """创建提示模板"""
        template = """
        请根据以下上下文信息回答问题。如果上下文没有提供足够的信息，请如实告知你不知道答案。

        上下文:
        {context}

        问题: {question}

        请提供准确、简洁的回答:
        """
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def create_qa_chain(self, retriever):
        """创建问答链"""
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )

# 示例用法
if __name__ == "__main__":
    from vector_store import VectorStoreManager
    
    # 加载向量存储和检索器
    vs_manager = VectorStoreManager()
    retriever = vs_manager.get_retriever()
    
    # 创建生成器并问答
    generator = AnswerGenerator()
    qa_chain = generator.create_qa_chain(retriever)
    
    result = qa_chain({"query": "什么是 RAG?"})
    print("答案:", result["result"])
    print("来源文档:", result["source_documents"])