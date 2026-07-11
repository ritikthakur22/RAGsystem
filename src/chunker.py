from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP
from src.logger import setup_logger

logger = setup_logger(__name__)


def split_documents(
    documents: List[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[Document]:
    """Splits a list of documents into smaller chunks for the RAG pipeline."""
    if not documents:
        logger.warning("No documents provided to split.")
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
    )

    logger.info(
        f"Splitting {len(documents)} documents with chunk_size={chunk_size} and overlap={chunk_overlap}"
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Generated {len(chunks)} chunks.")

    return chunks
