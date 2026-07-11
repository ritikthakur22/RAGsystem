import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
)
from src.logger import setup_logger

logger = setup_logger(__name__)

EXTENSION_MAPPING = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".csv": CSVLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
    ".html": TextLoader,
    ".json": TextLoader,
    ".py": TextLoader,
    ".cpp": TextLoader,
    ".h": TextLoader,
    ".java": TextLoader,
    ".sh": TextLoader,
    ".ps1": TextLoader,
    ".log": TextLoader,
}


def load_document(file_path: str) -> List[Document]:
    """Loads a single document based on its extension."""
    ext = os.path.splitext(file_path)[-1].lower()

    loader_class = EXTENSION_MAPPING.get(ext)
    if not loader_class:
        logger.warning(
            f"Unknown extension {ext} for {file_path}. Defaulting to TextLoader."
        )
        loader_class = TextLoader

    try:
        if loader_class == TextLoader:
            loader = loader_class(file_path, encoding="utf-8")
        else:
            loader = loader_class(file_path)
        return loader.load()
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return []


def load_directory(directory_path: str) -> List[Document]:
    """Recursively loads all supported documents from a directory."""
    documents = []
    if not os.path.exists(directory_path):
        logger.error(f"Directory not found: {directory_path}")
        return documents

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.startswith("."):
                continue
            file_path = os.path.join(root, file)
            logger.info(f"Loading {file_path}...")
            docs = load_document(file_path)
            documents.extend(docs)

    logger.info(
        f"Successfully loaded {len(documents)} document pages/sections from {directory_path}."
    )
    return documents
