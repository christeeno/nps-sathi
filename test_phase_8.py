import os
import json
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import load_faiss_index, retrieve_context
from rag_engine.llm_interface import generate_rag_response

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
FAISS_INDEX = os.path.join(DATA_DIR, 'vector_index.faiss')
METADATA_PKL = os.path.join(DATA_DIR, 'vector_metadata.pkl')

def run_phase_8_tests():
    print("--- Starting Phase 8: Hallucination Prevention Verification ---")
    
    # Check for API Keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
            print("ERROR: Please create a .env file with OPENAI_API_KEY or GOOGLE_API_KEY to test.")
             # Don't fail the github action tests entirely
            return

    try:
        index, metadata = load_faiss_index(FAISS_INDEX, METADATA_PKL)
    except FileNotFoundError:
        print("ERROR: vector database not found. Please run Phase 3 first.")
        return

    test_queries = [
        ("What is NPS Tier 1?", "Valid Policy Query"),
        ("What is Bitcoin?", "Irrelevant Query")
    ]

    for query, description in test_queries:
        print(f"\n--- [Test] {description} ---")
        print(f"Q: {query}")
        
        # 1. Retrieve Context
        top_chunks = retrieve_context(query, index, metadata, k=3)
        print(f"Retrieved {len(top_chunks)} relevant chunks.")
        
        # 2. Generate Safe Response
        result = generate_rag_response(query, top_chunks)
        
        print("\nPipeline Output:")
        print(json.dumps(result, indent=4))
        
        if "Bitcoin" in query:
            # Our prompt logic combined with validation should either return the strict fallback 
            # from the LLM based on rules or out-of-scope if retrieval totally failed.
            assert "could not find this information" in result["answer"].lower() or "outside the scope" in result["answer"].lower(), "Failed to prevent hallucination!"
            assert len(result["sources"]) == 0, "Should not cite sources for hallucinations"
            print("✅ Hallucination correctly prevented.")
        else:
            assert len(result["sources"]) > 0, "Citations are missing!"
            print("✅ Grounded response successfully generated with citations.")

if __name__ == "__main__":
    run_phase_8_tests()
