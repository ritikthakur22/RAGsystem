import argparse


from src.logger import setup_logger
from src.indexer import index_directory
from src.retriever import retrieve_context
from src.generator import generate_answer, stream_answer
from src.watcher import start_watcher
from src.benchmark import run_benchmark
from config.settings import DOCUMENTS_DIR

logger = setup_logger("cli")


def ingest_documents():
    """Manually ingests all documents from the DOCUMENTS_DIR."""
    print("Starting incremental document ingestion...")
    index_directory(DOCUMENTS_DIR)
    print("Ingestion complete.")


def chat_loop():
    """Starts the interactive chat loop."""
    print(
        "Starting Cybersecurity RAG Assistant. Type 'exit' or 'quit' to stop.\n"
        "You can specify a category by typing '@category query' (e.g. '@Linux how to harden ssh?')"
    )
    while True:
        try:
            query = input("\n> ")
            if query.strip().lower() in ["exit", "quit"]:
                break
            if not query.strip():
                continue

            category = None
            if query.startswith("@"):
                parts = query.split(" ", 1)
                if len(parts) == 2:
                    category = parts[0][1:]
                    query = parts[1]

            print("Retrieving context...")
            docs = retrieve_context(query, category=category)
            print("Generating answer...")
            print("\n" + "=" * 50)
            stream_answer(query, docs)
            print("=" * 50)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            logger.error(f"Chat error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Local RAG Cybersecurity Knowledge System"
    )
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Ingest all documents from the documents directory",
    )
    parser.add_argument(
        "--chat", action="store_true", help="Start the interactive chat interface"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch the documents directory for new files and automatically ingest them",
    )
    parser.add_argument("--benchmark", action="store_true", help="Run performance benchmarks")

    args = parser.parse_args()

    if args.ingest:
        ingest_documents()
    elif args.chat:
        chat_loop()
    elif args.watch:
        start_watcher()
    elif args.benchmark:
        run_benchmark()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
