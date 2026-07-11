from langchain_core.documents import Document
from src.retriever import retrieve_context
from src.generator import generate_answer, format_docs

def test_pipeline_components():
    docs = [Document(page_content="Mock doc content", metadata={"source": "test.txt", "page": 1})]
    
    formatted = format_docs(docs)
    assert "test.txt" in formatted
    assert "Mock doc content" in formatted
    
    # We won't test generate_answer entirely as it queries Ollama, 
    # but we can verify it doesn't crash on empty docs
    answer = generate_answer("test", [])
    assert "I don't know" in answer
