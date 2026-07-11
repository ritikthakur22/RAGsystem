# Local RAG Cybersecurity Knowledge System

A fully local Retrieval-Augmented Generation (RAG) system for learning cybersecurity. Prioritizes low hardware usage, stability, modular architecture, and offline-first operation.

## Architecture & Features
- **Language:** Python
- **Framework:** LangChain
- **Vector Database:** ChromaDB
- **Embedding Model:** `nomic-embed-text` via Ollama
- **Generator:** `qwen2.5-coder:7b` via Ollama
- **Interface:** Python CLI
- **Features:** 
  - Incremental Indexing & Duplicate Detection via SHA-256
  - Metadata Filtering by Document Category (e.g., Linux, Windows)
  - Automatic Document Watcher (Hot-reload for new files)
  - Streaming LLM Responses
  - Configurable hardware limits to maintain low memory usage
  - Comprehensive Grounding and Hallucination Evaluation Suite

## Directory Structure
```text
RAGsystem/
├── config/
│   └── settings.py
├── data/
│   ├── archive/
│   ├── incoming/
│   └── processed/
│       └── hashes.json
├── documents/
│   ├── Bash/
│   ├── CISA/
│   ├── Linux/
│   ├── MITRE/
│   └── OWASP/
├── logs/
├── src/
│   ├── benchmark.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── generator.py
│   ├── indexer.py
│   ├── internet_fallback.py
│   ├── loader.py
│   ├── logger.py
│   ├── retriever.py
│   ├── vector_store.py
│   └── watcher.py
├── tests/
│   ├── eval.py
│   ├── test_chunker.py
│   ├── test_loader.py
│   ├── test_pipeline.py
│   └── test_vector_store.py
├── main.py
├── requirements.txt
├── tasktrack.md
└── README.md
```

## Installation & Configuration

1. **Clone/Create the structure and enter the project folder:**
   ```bash
   cd ~/RAGsystem
   ```

2. **Setup Python Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install Models:**
   Ensure Ollama is running and install the required embedding model:
   ```bash
   ollama pull nomic-embed-text
   ```

4. **Configuration:**
   Settings such as Chunk Size, Overlap, and Context Window can be found and modified in `config/settings.py`.

## Usage & CLI Commands

**1. Interactive Chat (with Streaming):**
   ```bash
   python main.py --chat
   ```
   *To use Metadata filtering, start your query with a category tag (matching a folder name in `documents/`). Example:*
   `@Linux how to harden ssh?`

**2. Manual Incremental Indexing:**
   ```bash
   python main.py --ingest
   ```
   *Note: Thanks to duplicate detection, you can run this safely anytime; it will only process new or modified files.*

**3. Automatic Document Watcher:**
   ```bash
   python main.py --watch
   ```
   *Runs in the background and instantly indexes any files dropped into the `documents/` folders.*

**4. Performance Benchmark:**
   ```bash
   python main.py --benchmark
   ```
   *Measures the exact latency for Document Loading, Chunking, Embedding, DB Insertion, Retrieval, and Generation on your hardware.*

## Troubleshooting

- **Out of Memory Issues?** Check `config/settings.py` and ensure `CONTEXT_WINDOW` remains low (e.g., 4096).
- **Missing Module Errors?** Ensure you have activated the virtual environment and set `PYTHONPATH=.` when running tests manually.
- **Documents not indexing?** Check `data/processed/hashes.json` to verify if the file was already indexed and its hash hasn't changed.

## Future Roadmap

- Phase 2: Web UI & Voice Interface
- Phase 3: Multi-agent Architecture
- Phase 4: Code & Git Repository indexing
- Phase 5: Internet Fallback (Module stub created)


Resume: agy --conversation=7b06bfa7-9288-4892-8dfc-1a4d6956b58a (or -c)

