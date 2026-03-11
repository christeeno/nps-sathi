import json
import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_pipeline.intent_classifier import classify_intent
from decision_engine.recommendation_engine import recommend_pension_scheme
from evaluation.rag_evaluator import evaluate_rag_accuracy

def evaluate_intent_routing(dataset_path: str) -> float:
    """
    Verifies that the intent classifier properly routes test queries
    to the anticipated engines.
    """
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
        
    correct = 0
    total = len(dataset)
    
    if total == 0:
        return 100.0
        
    for item in dataset:
        query = item["question"]
        expected_intent = item["expected_intent"]
        
        predicted = classify_intent(query)
        if predicted == expected_intent:
            correct += 1
            
    score = (correct / total) * 100
    return round(score, 2)

def evaluate_recommendation_consistency() -> float:
    """
    Tests the decision_engine logic against known static rule sets.
    """
    # Test Case 1: Govt Employee, High Tenure, Low Risk -> UPS
    p1 = {
        "age": 45,
        "years_of_service": 15,
        "risk_preference": "low",
        "government_employee": True
    }
    rec1 = recommend_pension_scheme(p1)
    pass1 = (rec1["recommended_scheme"] == "UPS")
    
    # Test Case 2: Private Employee / General -> NPS
    p2 = {
        "age": 30,
        "years_of_service": 5,
        "risk_preference": "moderate",
        "government_employee": False
    }
    rec2 = recommend_pension_scheme(p2)
    pass2 = (rec2["recommended_scheme"] == "NPS")
    
    # Calculate score
    total = 2
    correct = sum([pass1, pass2])
    score = (correct / total) * 100
    return round(score, 2)

def generate_evaluation_report(dataset_path: str, rag_index=None, rag_metadata=None) -> dict:
    """
    Orchestrates the evaluation modules and formats the final report.
    """
    rag_score = 0.0
    if rag_index is not None and rag_metadata is not None:
        rag_score = evaluate_rag_accuracy(dataset_path, rag_index, rag_metadata)
        
    routing_score = evaluate_intent_routing(dataset_path)
    decision_score = evaluate_recommendation_consistency()
    
    return {
        "rag_accuracy": rag_score,
        "routing_accuracy": routing_score,
        "decision_engine_consistency": decision_score
    }
