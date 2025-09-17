# chat_robot
Indexing: a pipeline for ingesting data from a source and indexing it. This usually happens offline. include load , split and store

Retrieval and generation: the actual RAG chain, which takes user query at run time and retrieves the relevant data from the index, then pass that to the model.


# first step 

langsmith api: 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

rag_project/
│
├── src/                             # 源代码目录
│   ├── __init__.py
│   ├── main.py                      # 主程序入口
│   ├── config/                      # 配置模块
│   │   ├── __init__.py
│   │   └── settings.py              # 应用设置
│   ├── core/                        # 核心功能模块
│   │   ├── __init__.py
│   │   ├── document_processing.py   # 文档加载与处理
│   │   ├── vector_store.py          # 向量数据库操作
│   │   ├── retrieval.py             # 检索功能
│   │   └── generation.py            # 生成功能
│   ├── models/                      # 数据模型定义
│   │   ├── __init__.py
│   │   └── schemas.py               # Pydantic 模型
│   ├── utils/                       # 工具函数
│   │   ├── __init__.py
│   │   └── helpers.py               # 辅助函数
│   └── web/                         # Web 接口 (可选)
│       ├── __init__.py
│       ├── api.py                   # FastAPI 路由
│       └── templates/               # Jinja2 模板
│
├── data/                            # 数据目录
│   ├── raw/                         # 原始文档
│   └── processed/                   # 处理后的数据
│
├── tests/                           # 测试目录
│   ├── __init__.py
│   ├── test_document_processing.py
│   └── test_retrieval.py
│
├── storage/                         # 向量数据库存储目录
│
├── requirements.txt                 # 项目依赖
├── .env.example                     # 环境变量示例
├── .gitignore                      # Git 忽略规则
└── README.md                       # 项目说明文档