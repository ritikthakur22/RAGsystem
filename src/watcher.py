import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.indexer import index_file, load_hashes
from config.settings import DOCUMENTS_DIR
from src.logger import setup_logger

logger = setup_logger(__name__)


class DocumentHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.hashes = load_hashes()

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        # Ignore hidden files or .gitkeep
        if os.path.basename(filepath).startswith("."):
            return

        # Allow some time for the file to be completely written to disk
        time.sleep(1)
        self.process_file(filepath)

    def on_modified(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        if os.path.basename(filepath).startswith("."):
            return

        time.sleep(1)
        self.process_file(filepath)

    def process_file(self, filepath: str):
        logger.info(f"File event detected: {filepath}")
        index_file(filepath, self.hashes)


def start_watcher():
    """Starts watching the documents directory for new files."""
    if not os.path.exists(DOCUMENTS_DIR):
        logger.error(f"Documents directory {DOCUMENTS_DIR} does not exist.")
        return

    event_handler = DocumentHandler()
    observer = Observer()
    observer.schedule(event_handler, DOCUMENTS_DIR, recursive=True)
    observer.start()

    logger.info(f"Started watching directory: {DOCUMENTS_DIR}")
    print(f"Watching {DOCUMENTS_DIR} for new files. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Stopping watcher...")
    observer.join()
