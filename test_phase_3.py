import os
from rag_engine import (
    load_chunks_from_json,
    generate_embeddings,
    create_faiss_index,
    load_faiss_index,
    retrieve_context
)

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
CHUNKS_JSON = os.path.join(DATA_DIR, 'processed_chunks.json')
FAISS_INDEX = os.path.join(DATA_DIR, 'vector_index.faiss')
METADATA_PKL = os.path.join(DATA_DIR, 'vector_metadata.pkl')

def run_phase_3():
    print("--- Starting Phase 3: Vector Database Creation ---")
    
    # 1. Load the processed deterministic chunks
    chunks = load_chunks_from_json(CHUNKS_JSON)
    if not chunks:
        print("No chunks found. Run Phase 2 script first.")
        return
        
    print(f"Loaded {len(chunks)} chunks.")

    # 2. Generate Embeddings using all-MiniLM-L6-v2
    embeddings, metadata = generate_embeddings(chunks)

    # 3. Create FAISS index
    create_faiss_index(embeddings, metadata, FAISS_INDEX, METADATA_PKL)
    
    # 4. Test Retrieval
    print("\n--- Testing Retrieval Pipeline ---")
    index, saved_metadata = load_faiss_index(FAISS_INDEX, METADATA_PKL)
    
    test_query = "What are the withdrawal rules for NPS?"
    print(f"Test Query: '{test_query}'\n")
    
    top_chunks = retrieve_context(test_query, index, saved_metadata, k=3)
    
    for i, res in enumerate(top_chunks):
        chunk = res["chunk"]
        print(f"Result {i+1} (Score: {res['score']:.4f}):")
        print(f"  Chunk ID: {chunk.get('chunk_id')}")
        print(f"  Source:   {chunk.get('source')}")
        print(f"  Text:     {chunk.get('text')}\n")

if __name__ == "__main__":
    run_phase_3()
