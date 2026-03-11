import json
import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_pipeline.pipeline_controller import handle_query

def run_phase_9_tests():
    print("--- Starting Phase 9: AI Pipeline Integration Verification ---\n")
    
    user_profile = {
        "age": 30,
        "salary": 80000,
        "monthly_contribution": 5000,
        "risk_preference": "moderate",
        "years_of_service": 5,
        "government_employee": False,
        "retirement_age": 60,
        "expected_return": 0.10,
        "volatility": 0.15
    }

    test_queries = [
        ("What is NPS Tier 1?", "knowledge_query"),
        ("How much pension if I invest 5000?", "retirement_forecast"),
        ("Should I choose NPS or UPS?", "investment_recommendation")
    ]

    for query, expected_intent in test_queries:
        print(f"\n[Test] Query: '{query}'")
        
        result = handle_query(query, user_profile)
        
        print("\nUnified Pipeline Output:")
        # We handle any missing keys gracefully in printing
        print(json.dumps({
            "intent": result.get("intent"),
            "response": result.get("response", "")[:150] + "..." if len(result.get("response", "")) > 150 else result.get("response", ""),
            "sources_count": len(result.get("sources", [])),
            "financial_data_keys": list(result.get("financial_data", {}).keys())
        }, indent=4))
        
        assert result.get("intent") == expected_intent, f"Failed to route intent properly! Expected {expected_intent}, got {result.get('intent')}"
        print(f"✅ Successfully routed to and evaluated by the {expected_intent} engine.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    run_phase_9_tests()
