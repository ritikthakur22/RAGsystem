import os
from src.loader import load_document

def test_loader_text_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello Cybersecurity World")
    
    docs = load_document(str(test_file))
    assert len(docs) == 1
    assert "Hello Cybersecurity World" in docs[0].page_content
