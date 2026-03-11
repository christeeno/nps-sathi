import json
import logging
import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_engine.llm_interface import generate_rag_response
from rag_engine.vector_db import retrieve_context

logger = logging.getLogger(__name__)

def evaluate_rag_accuracy(dataset_path: str, index, metadata) -> float:
    """
    Evaluates the accuracy of the RAG engine against expected keywords.
    Steps:
    1. Send questions to the pipeline.
    2. Check if expected keywords appear in the generated answer.
    3. Calculate overall accuracy score.
    """
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
        
    rag_queries = [item for item in dataset if item["expected_intent"] == "knowledge_query"]
    correct = 0
    total = len(rag_queries)
    
    if total == 0:
        return 100.0
        
    for item in rag_queries:
        query = item["question"]
        expected_keywords = [k.lower() for k in item["expected_keywords"]]
        
        # Retrieve context
        top_chunks = retrieve_context(query, index, metadata, k=3)
        
        # Generate response
        result = generate_rag_response(query, top_chunks)
        response_text = result.get("answer", "").lower()
        
        # Validate against keywords
        all_keywords_found = True
        for kw in expected_keywords:
            if kw not in response_text:
                all_keywords_found = False
                logger.debug(f"Missing expected keyword '{kw}' for query: '{query}'")
                
        if all_keywords_found:
            correct += 1
            
    score = (correct / total) * 100
    return round(score, 2)
