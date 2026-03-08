import os
from rag_engine import load_faiss_index, retrieve_context, generate_rag_response

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
FAISS_INDEX = os.path.join(DATA_DIR, 'vector_index.faiss')
METADATA_PKL = os.path.join(DATA_DIR, 'vector_metadata.pkl')

def run_phase_4_tests():
    print("--- Starting Phase 4: RAG AI Pipeline Verification ---")
    
    # Check for API Keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: Please create a .env file with OPENAI_API_KEY or GOOGLE_API_KEY to test.")
        return
        
    try:
        index, metadata = load_faiss_index(FAISS_INDEX, METADATA_PKL)
    except FileNotFoundError:
        print("ERROR: vector database not found. Please run Phase 3 first.")
        return

    test_queries = [
        "What is NPS Tier 1?",
        "What happens if I withdraw early?",
        "What is bitcoin?" # Negative Test
    ]

    for i, query in enumerate(test_queries):
        print(f"\n--- Test Query {i+1} ---")
        print(f"Q: {query}")
        
        # 1. Retrieve Context
        top_chunks = retrieve_context(query, index, metadata, k=3)
        print(f"Retrieved {len(top_chunks)} relevant chunks from policy documentation.")
        
        # 2. Generate Response
        response = generate_rag_response(query, top_chunks)
        print("\nAI Response:")
        print(f"> {response}\n")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    run_phase_4_tests()
