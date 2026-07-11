from langchain_core.documents import Document
from src.vector_store import get_vector_store, add_documents_to_store

def test_vector_store():
    # Only run a very small test document to avoid hitting embedding limits or slowing down tests too much
    doc = Document(page_content="Test cybersecurity concept: Defense in depth.", metadata={"source": "test.txt"})
    
    add_documents_to_store([doc])
    
    store = get_vector_store()
    results = store.similarity_search("Defense in depth", k=1)
    
    assert len(results) == 1
    assert "Defense in depth" in results[0].page_content
