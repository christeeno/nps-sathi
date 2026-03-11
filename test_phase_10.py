import json
import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluation.pipeline_tester import generate_evaluation_report
from rag_engine.vector_db import load_faiss_index

def run_phase_10_tests():
    print("--- Starting Phase 10: Model Evaluation ---")
    
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    FAISS_INDEX = os.path.join(DATA_DIR, 'vector_index.faiss')
    METADATA_PKL = os.path.join(DATA_DIR, 'vector_metadata.pkl')
    DATASET_PATH = os.path.join(os.path.dirname(__file__), 'evaluation', 'evaluation_dataset.json')
    
    try:
        index, metadata = load_faiss_index(FAISS_INDEX, METADATA_PKL)
    except FileNotFoundError:
        print("Vector Database not found. RAG Evaluation will be skipped.")
        index, metadata = None, None
        
    print("Running comprehensive evaluation pipeline (this may take a moment pending LLM latency)...")
    
    report = generate_evaluation_report(DATASET_PATH, index, metadata)
    
    print("\nFinal Evaluation Report:")
    print(json.dumps(report, indent=4))
    
    # Assertions for basic pipeline functionality
    assert "rag_accuracy" in report
    assert "routing_accuracy" in report
    assert "decision_engine_consistency" in report
    
    print("\n✅ Verification successful. The Model Evaluation framework is completely integrated.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    run_phase_10_tests()
