import time
import os
import threading
from src.indexer import index_file, load_hashes
from src.retriever import retrieve_context
from src.generator import generate_answer
from config.settings import DOCUMENTS_DIR
from src.vector_store import get_vector_store
from src.watcher import start_watcher

def test_1_grounded_response():
    file_path = os.path.join(DOCUMENTS_DIR, "test_apple.txt")
    with open(file_path, "w") as f:
        f.write("The apple is blue.")
    
    hashes = load_hashes()
    index_file(file_path, hashes)
    
    docs = retrieve_context("What color is the apple?")
    assert len(docs) > 0, "Failed to retrieve the document."
    
    answer = generate_answer("What color is the apple?", docs)
    assert "blue" in answer.lower(), "Hallucinated or incorrect answer."
    assert "test_apple.txt" in answer, "Source citation missing."
    print("Test 1 (Grounded Response) Passed.")

def test_2_hallucination_resistance():
    docs = retrieve_context("What is the wingspan of a Martian dragon?")
    answer = generate_answer("What is the wingspan of a Martian dragon?", docs)
    assert "don't know" in answer.lower() or "not found" in answer.lower() or "no information" in answer.lower() or "cannot answer" in answer.lower() or "not mention" in answer.lower() or "doesn't know" in answer.lower() or "does not know" in answer.lower(), f"Model hallucinated an answer! Answer was: {answer}"
    print("Test 2 (Hallucination Resistance) Passed.")

def test_3_persistence():
    store = get_vector_store()
    results = store.similarity_search("The apple is blue.")
    assert len(results) > 0, "Persistence failed, document not found after re-init."
    print("Test 3 (Persistence) Passed.")

def test_4_watcher():
    file_path = os.path.join(DOCUMENTS_DIR, "test_watcher.txt")
    if os.path.exists(file_path):
        os.remove(file_path)
        
    watcher_thread = threading.Thread(target=start_watcher, daemon=True)
    watcher_thread.start()
    
    time.sleep(2)
    
    with open(file_path, "w") as f:
        f.write("This is a watcher test file.")
        
    time.sleep(5)
    
    store = get_vector_store()
    results = store.similarity_search("watcher test file")
    
    # Clean up
    os.remove(file_path)
    os.remove(os.path.join(DOCUMENTS_DIR, "test_apple.txt"))
    
    assert len(results) > 0, "Watcher failed to index the new file."
    print("Test 4 (Watcher Auto-indexing) Passed.")

if __name__ == "__main__":
    print("Running Evaluation Suite (Grounding Tests)...")
    test_1_grounded_response()
    test_2_hallucination_resistance()
    test_3_persistence()
    test_4_watcher()
    print("All evaluation tests passed!")
