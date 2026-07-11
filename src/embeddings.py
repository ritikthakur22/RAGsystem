from langchain_ollama import OllamaEmbeddings
from config.settings import EMBEDDING_MODEL
from src.logger import setup_logger

logger = setup_logger(__name__)


def get_embedding_model() -> OllamaEmbeddings:
    """Initializes and returns the local Ollama embedding model."""
    logger.info(f"Initializing embedding model: {EMBEDDING_MODEL}")
    try:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        return embeddings
    except Exception as e:
        logger.error(f"Failed to initialize embedding model: {e}")
        raise
