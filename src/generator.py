from typing import List
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import GENERATION_MODEL, TEMPERATURE
from src.logger import setup_logger

logger = setup_logger(__name__)


def get_prompt_template() -> ChatPromptTemplate:
    """Builds the prompt template for the RAG system."""
    template = """You are a cybersecurity assistant. 
If the user is just greeting you (e.g., "hi", "hello"), respond naturally and friendly in the "Final answer" section, and put "N/A" for the documents.
For all other questions, use the following retrieved context to answer. If you don't know the answer based on the context, just say that you don't know. Do not use outside knowledge.

Your answer MUST strictly follow this format:
1. Final answer
2. Supporting document names
3. Page numbers when available
4. Confidence level (High, Medium, Low) based on how well the context covers the answer.

Never answer from retrieved context without indicating the source.

Context:
{context}

Question: {question}

Answer:"""
    return ChatPromptTemplate.from_template(template)


def format_docs(docs: List[Document]) -> str:
    """Formats the retrieved documents into a single string with metadata."""
    formatted = []
    for d in docs:
        source = d.metadata.get("source", "Unknown")
        page = d.metadata.get("page", "N/A")
        formatted.append(f"[Source: {source}, Page: {page}]\n{d.page_content}")
    return "\n\n".join(formatted)


def get_llm() -> ChatOllama:
    """Connects to the local Ollama generator model."""
    logger.info(f"Initializing LLM: {GENERATION_MODEL}")
    from config.settings import CONTEXT_WINDOW

    return ChatOllama(
        model=GENERATION_MODEL, temperature=TEMPERATURE, num_ctx=CONTEXT_WINDOW
    )


def generate_answer(query: str, retrieved_docs: List[Document]) -> str:
    """Generates an answer using the retrieved documents and the LLM."""
    if not retrieved_docs:
        return "I don't know. (No context retrieved)"

    prompt = get_prompt_template()
    llm = get_llm()
    output_parser = StrOutputParser()

    context_str = format_docs(retrieved_docs)
    logger.info(f"Generating answer for query: '{query}'")

    chain = prompt | llm | output_parser

    answer = chain.invoke({"context": context_str, "question": query})

    return answer

def stream_answer(query: str, retrieved_docs: List[Document]):
    """Streams the answer directly to stdout, with Internet Fallback support."""
    if not retrieved_docs:
        print("I don't know. (No context retrieved)")
        return

    prompt = get_prompt_template()
    llm = get_llm()
    output_parser = StrOutputParser()

    context_str = format_docs(retrieved_docs)
    logger.info(f"Streaming answer for query: '{query}'")

    chain = prompt | llm | output_parser

    full_response = ""
    for chunk in chain.stream({"context": context_str, "question": query}):
        print(chunk, end="", flush=True)
        full_response += chunk
    print()

    # --- Internet Fallback ---
    if "I don't know." in full_response:
        print("\n[!] Local knowledge insufficient. Initiating Phase 5 Internet Fallback...\n")
        from src.internet_fallback import fallback_module
        internet_context = fallback_module.search_internet(query)
        
        logger.info(f"Streaming fallback answer for query: '{query}'")
        for chunk in chain.stream({"context": internet_context, "question": query}):
            print(chunk, end="", flush=True)
        print()
