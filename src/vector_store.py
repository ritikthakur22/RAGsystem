from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from src.embeddings import get_embedding_model
from config.settings import VECTOR_DB_DIR
from src.logger import setup_logger

logger = setup_logger(__name__)

COLLECTION_NAME = "cybersecurity_knowledge"


def get_vector_store() -> Chroma:
    """Returns the Chroma vector store instance."""
    embedding_model = get_embedding_model()

    logger.info(f"Connecting to ChromaDB at {VECTOR_DB_DIR}")
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=VECTOR_DB_DIR,
    )

    return vector_store


def add_documents_to_store(chunks: List[Document]) -> None:
    """Adds chunked documents to the ChromaDB vector store."""
    if not chunks:
        logger.warning("No chunks to add to vector store.")
        return

    vector_store = get_vector_store()

    logger.info(f"Adding {len(chunks)} chunks to vector store...")
    vector_store.add_documents(documents=chunks)
    logger.info("Successfully added chunks to vector store.")
