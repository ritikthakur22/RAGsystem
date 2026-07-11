import time
import os
from typing import List
from langchain_core.documents import Document
from src.loader import load_document
from src.chunker import split_documents
from src.vector_store import add_documents_to_store, get_vector_store
from src.retriever import retrieve_context
from src.generator import generate_answer
from src.logger import setup_logger

logger = setup_logger("benchmark")

def run_benchmark():
    print("Starting Performance Benchmark...\n")
    
    # 1. Create a dummy file
    dummy_file = "benchmark_dummy.txt"
    with open(dummy_file, "w") as f:
        f.write("This is a benchmark document for cybersecurity. " * 100)
        
    try:
        total_start = time.time()
        
        # Benchmark Loading
        start = time.time()
        docs = load_document(dummy_file)
        load_time = time.time() - start
        print(f"Document Loading Time: {load_time:.4f} seconds")
        
        # Benchmark Chunking
        start = time.time()
        chunks = split_documents(docs)
        chunk_time = time.time() - start
        print(f"Chunking Time: {chunk_time:.4f} seconds")
        
        # Benchmark Embedding & Insertion
        start = time.time()
        add_documents_to_store(chunks)
        embed_time = time.time() - start
        print(f"Embedding & DB Insertion Time: {embed_time:.4f} seconds")
        
        # Benchmark Retrieval
        query = "cybersecurity benchmark"
        start = time.time()
        retrieved = retrieve_context(query)
        retrieve_time = time.time() - start
        print(f"Retrieval Latency: {retrieve_time:.4f} seconds")
        
        # Benchmark Generation
        start = time.time()
        answer = generate_answer(query, retrieved)
        gen_time = time.time() - start
        print(f"Generation Latency: {gen_time:.4f} seconds")
        
        total_time = time.time() - total_start
        print(f"\nTotal Runtime: {total_time:.4f} seconds")
        
    finally:
        if os.path.exists(dummy_file):
            os.remove(dummy_file)
