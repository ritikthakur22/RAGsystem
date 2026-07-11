from typing import List
from langchain_core.documents import Document
from src.vector_store import get_vector_store
from config.settings import TOP_K_RETRIEVAL
from src.logger import setup_logger

logger = setup_logger(__name__)


def retrieve_context(query: str, top_k: int = TOP_K_RETRIEVAL, category: str = None) -> List[Document]:
    """Retrieves the most relevant document chunks for a given query."""
    logger.info(f"Retrieving top {top_k} documents for query: '{query}'")
    vector_store = get_vector_store()

    search_kwargs = {"k": top_k}
    if category:
        search_kwargs["filter"] = {"category": category}

    retriever = vector_store.as_retriever(search_kwargs=search_kwargs)
    docs = retriever.invoke(query)

    logger.info(f"Retrieved {len(docs)} documents.")
    return docs
