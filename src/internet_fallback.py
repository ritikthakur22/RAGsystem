from src.logger import setup_logger
from duckduckgo_search import DDGS
from langchain_core.documents import Document

logger = setup_logger(__name__)

class InternetFallbackModule:
    """
    Internet Fallback capabilities using DuckDuckGo Search.
    """

    def __init__(self):
        logger.info("Internet Fallback Module initialized.")

    def search_internet(self, query: str, num_results: int = 3) -> str:
        """Perform a web search using DuckDuckGo."""
        logger.info(f"Performing Internet search for: '{query}'")
        try:
            ddgs = DDGS()
            results = ddgs.text(query, max_results=num_results)
            if not results:
                return "No useful information found on the internet."
            
            context = ""
            for r in results:
                title = r.get('title', 'No Title')
                body = r.get('body', 'No Content')
                link = r.get('href', 'No Link')
                context += f"[Source: INTERNET - {title} ({link})]\n{body}\n\n"
            
            return context
        except Exception as e:
            logger.error(f"Internet search failed: {e}")
            return f"Internet search failed: {e}"

fallback_module = InternetFallbackModule()
