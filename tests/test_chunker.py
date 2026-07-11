from langchain_core.documents import Document
from src.chunker import split_documents

def test_split_documents():
    long_text = "A" * 1000
    doc = Document(page_content=long_text)
    
    # Using 500 chunk size and 100 overlap
    chunks = split_documents([doc], chunk_size=500, chunk_overlap=100)
    
    # 1000 length with 500 chunks and 100 overlap:
    # chunk 1: 0-500 (length 500)
    # chunk 2: 400-900 (length 500)
    # chunk 3: 800-1000 (length 200)
    assert len(chunks) == 3
    assert len(chunks[0].page_content) == 500
    assert len(chunks[2].page_content) == 200
