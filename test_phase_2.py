import os
from rag_engine import load_documents, clean_documents, chunk_documents, save_chunks_to_json, load_chunks_from_json

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
OUTPUT_JSON = os.path.join(DATA_DIR, 'processed_chunks.json')

def run_phase_2():
    print("--- Starting Phase 2: Data Ingestion ---")
    
    # 1. Load documents
    docs = load_documents(DATA_DIR)
    if not docs:
        print("No documents found in 'data/' directory.")
        return

    # 2. Clean documents
    # The clean_documents function expects a list of documents and cleans the page_content
    # The current implementation of clean_documents modifies in place, but we need to ensure we clean it correctly:
    for doc in docs:
        import re
        text = doc.page_content
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        doc.page_content = text.strip()

    # 3. Chunk documents
    chunks = chunk_documents(docs, chunk_size=500, chunk_overlap=50)
    
    # 4. Save to JSON
    save_chunks_to_json(chunks, OUTPUT_JSON)

    # 5. Verify by loading
    loaded_chunks = load_chunks_from_json(OUTPUT_JSON)
    print("\n--- Verification: Printing first 2 chunks ---")
    for i, c in enumerate(loaded_chunks[:2]):
        print(f"\nChunk {i+1}:\n{c['content']}")

if __name__ == "__main__":
    run_phase_2()
