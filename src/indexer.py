import os
import hashlib
import json
from typing import List
from langchain_core.documents import Document
from src.loader import load_document
from src.chunker import split_documents
from src.vector_store import add_documents_to_store, get_vector_store
from config.settings import DATA_DIR, DOCUMENTS_DIR
from src.logger import setup_logger

logger = setup_logger(__name__)

HASH_FILE = os.path.join(DATA_DIR, "processed", "hashes.json")

def load_hashes() -> dict:
    if os.path.exists(HASH_FILE):
        try:
            with open(HASH_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Failed to read hashes.json. Starting fresh.")
    return {}

def save_hashes(hashes: dict):
    os.makedirs(os.path.dirname(HASH_FILE), exist_ok=True)
    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

def compute_sha256(filepath: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_category(filepath: str) -> str:
    """Extracts category from the folder name directly under DOCUMENTS_DIR."""
    rel_path = os.path.relpath(filepath, DOCUMENTS_DIR)
    parts = rel_path.split(os.sep)
    if len(parts) > 1:
        return parts[0]
    return "Uncategorized"

def index_file(filepath: str, hashes: dict) -> bool:
    """Indexes a single file if it is new or modified. Returns True if indexed."""
    if not os.path.exists(filepath):
        return False
        
    rel_key = os.path.relpath(filepath, DOCUMENTS_DIR)
    current_hash = compute_sha256(filepath)
    
    # Check against both relative and legacy absolute paths
    if (rel_key in hashes and hashes[rel_key] == current_hash) or \
       (filepath in hashes and hashes[filepath] == current_hash):
        logger.info(f"Skipping {filepath} (Unchanged).")
        return False
        
    logger.info(f"Indexing {filepath}...")
    docs = load_document(filepath)
    if not docs:
        logger.warning(f"Failed to load or empty document: {filepath}")
        return False
        
    # Inject metadata
    category = get_category(filepath)
    for doc in docs:
        doc.metadata["category"] = category
        doc.metadata["source"] = os.path.basename(filepath)
        doc.metadata["rel_path"] = rel_key
        
    chunks = split_documents(docs)
    add_documents_to_store(chunks)
    
    hashes[rel_key] = current_hash
    save_hashes(hashes)
    logger.info(f"Successfully indexed {filepath}")
    return True

def index_directory(directory_path: str):
    """Incrementally indexes a directory."""
    hashes = load_hashes()
    indexed_count = 0
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.startswith('.'):
                continue
            filepath = os.path.join(root, file)
            if index_file(filepath, hashes):
                indexed_count += 1
                
    logger.info(f"Incremental indexing complete. Indexed {indexed_count} new/modified files.")
