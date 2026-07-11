import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vectordb")

# Chunking Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Retrieval Settings
TOP_K_RETRIEVAL = 10

# Model Settings
EMBEDDING_MODEL = "nomic-embed-text"
GENERATION_MODEL = "qwen2.5-coder:7b"
CONTEXT_WINDOW = 4096
TEMPERATURE = 0.2
